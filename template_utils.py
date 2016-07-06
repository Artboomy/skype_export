#! python3
# -*- coding: utf-8 -*-
import os
from utils import get_cur_time_filename
from jinja2 import Template as jTemplate
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render_message(msg):
    msg_id = msg['id']
    time_stamp = msg['time_stamp']
    author_name = msg['author']
    text = msg['msg_text']
    is_mine = None  # msg.is_mine
    with open('static/msg_template.html', 'rt') as template_file:
        template_string = template_file.read()
        template = jTemplate(template_string)
        result = template.render(
            msg_id=msg_id, time_stamp=time_stamp, author=author_name, text=text, is_mine=is_mine
        )
    return result


def render_message_list(msg_list):
    env = Environment()
    env.loader = FileSystemLoader('.')
    template = env.get_template('static/msg_list_template.html')
    return template.render(msg_list=msg_list)


def export_messages(msg_list, output_file_name=None):
    if output_file_name is None:
        dir_name = str(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.exists(dir_name + '/export/'):
            os.makedirs(dir_name + '/export/')
        output_file_name = 'export/{0}.html'.format(get_cur_time_filename())

    with open(output_file_name, 'wt', encoding='utf-8') as out_file:
        out_file.write(render_message_list(msg_list))
        print('export successful to file: ', output_file_name)
