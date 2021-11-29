# -*- coding: utf8 -*-
#

class ConstituencyLabelException(Exception):
    """base exception"""
    msg = 'constituency label base exception'

    def __init__(self, msg: str = ''):
        if msg:
            self.msg = msg

    def __repr__(self):
        return self.msg


class DuplicateIdException(ConstituencyLabelException):
    msg = 'id duplicate error'


class LeaveNodeLengthError(ConstituencyLabelException):
    msg = 'unknown error'
