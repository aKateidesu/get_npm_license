# Author: aKateidesu

from json import load
from re import search
from enum import Enum
from requests import get
from concurrent.futures import ThreadPoolExecutor
from pandas import DataFrame
from tqdm import tqdm

DEPENDENCIES_KEY = 'dependencies'
DEV_DEPENDENCIES_KEY = 'devDependencies'
NPM_BASE_URL = 'https://www.npmjs.com/package/'
REG_MATCH_LICENSE = r'"license":"[^,]+"'


class ParseTarget(Enum):
    ALL = 1,
    RELEASE = 2,
    DEV = 3


PARSE_TARGET = ParseTarget.ALL


def parse_package_json(package_json: str) -> tuple[dict, dict]:
    with open(package_json, 'r') as f:
        json_dict: dict = load(f)
    return json_dict.get(DEPENDENCIES_KEY), json_dict.get(DEV_DEPENDENCIES_KEY)


def retrieve_npm_info(package_name: str) -> dict:
    url = NPM_BASE_URL + package_name
    response_str = get(url).text
    return {package_name: search(REG_MATCH_LICENSE, response_str)[0].split('"')[-2]}


def main(json_file_path: str, output_file_path: str, parse_target: ParseTarget = ParseTarget.ALL, max_thread: int = 4) -> None:
    # 线程池
    thread_pool = ThreadPoolExecutor(max_thread)

    dependencies, dev_dependencies = parse_package_json(json_file_path)
    if parse_target == ParseTarget.RELEASE:
        target_dependencies = list(dependencies.keys())
    elif parse_target == ParseTarget.DEV:
        target_dependencies = list(dev_dependencies.keys())
    else:
        target_dependencies = list(set(list(dependencies.keys()) + list(dev_dependencies.keys())))

    pool_results = [thread_pool.submit(retrieve_npm_info, dependency) for dependency in target_dependencies]

    results = [result.result() for result in tqdm(pool_results, unit='file')]

    df = DataFrame({
        'Package': [list(result.keys())[0] for result in results],
        'License': [list(result.values())[0] for result in results]
    })
    df.to_excel(output_file_path)
