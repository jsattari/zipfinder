#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def allowed_file(filename, verification_list):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in verification_list
