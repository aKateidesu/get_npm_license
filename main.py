# Author: aKateidesu

from services import main, ParseTarget
from argparse import ArgumentParser

JSON_FILE_PATH = "./package.json"
OUTPUT_EXCEL_PATH = './output.xlsx'
MAX_THREADS = 4
PARSE_TARGET = ParseTarget.ALL

PARSER = ArgumentParser(description='获取npm的license信息')
PARSER.add_argument('-f', '--file', default=JSON_FILE_PATH, help='npm的json文件路径')
PARSER.add_argument('-o', '--output', default=OUTPUT_EXCEL_PATH, help='输出的xlsx文件路径')
PARSER.add_argument('-t', '--target', default=PARSE_TARGET.name, help='是否解析npm的devDependencies(ALL、Release、DEV)')
PARSER.add_argument('-m', '--max', default=str(MAX_THREADS), help='发起request请求的最大线程数')

if __name__ == '__main__':
    args = PARSER.parse_args()
    if args.file:
        JSON_FILE_PATH = str(args.file).strip()
    if args.output:
        OUTPUT_EXCEL_PATH = str(args.output).strip()
    if args.target:
        PARSE_TARGET = ParseTarget[args.target]
    if args.max:
        MAX_THREADS = int(args.max)

    main(JSON_FILE_PATH, OUTPUT_EXCEL_PATH, PARSE_TARGET, MAX_THREADS)
