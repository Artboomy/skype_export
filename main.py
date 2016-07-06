#! python3
# -*- coding: utf-8 -*-

from logic import Logic
import argparse
import template_utils as tu
parser = argparse.ArgumentParser()


def init_args():
    args_dict = (
        {'short': '-em', 'long': '--export_messages',
         'help': 'export messages', 'action': 'store_true'},
        {'short': '-u', 'long': '--user_name',
         'help': 'messages with this user', 'action': 'store'},
        {'short': '-ds', 'long': '--date_start',
         'help': 'messages from this date, in yyyy-mm-dd format', 'action': 'store'},
        {'short': '-de', 'long': '--date_end',
         'help': 'messages up to this date, in yyyy-mm-dd format', 'action': 'store'},
        {'short': '-o', 'long': '--output_file',
         'help': 'output filename', 'action': 'store'}
    )
    for arg in args_dict:
        parser.add_argument(arg['short'], arg['long'], help=arg['help'], action=arg['action'])

init_args()
args = parser.parse_args()
if args.export_messages:
    if args.user_name is None:
        raise AttributeError('Username not specified')
    BL = Logic()
    messages = BL.get_messages(args.user_name, time_start=args.date_start, time_end=args.date_end)
    tu.export_messages(messages, args.output_file)
