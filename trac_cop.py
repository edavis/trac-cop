"""
trac_cop.py -- write tickets
"""

import re
import sys
import email
import argparse
from trac.ticket import Ticket
from trac.env import open_environment

bcc_msg = lambda msg: 'delivered-to' in msg and 'trac' in msg['delivered-to']
to_msg = lambda msg: 'to' in msg and 'trac' in msg['to']

def get_ticket_id(address):
    """
    Get the ticket ID out of the `To` or `Delivered-To` header.
    """
    match = re.search('^trac\+(\d+)@', address)
    if match:
        return int(match.group(1))

def get_ticket(env, msg):
    """
    Return the appropriate Trac ticket.
    """
    address = msg['delivered-to'] or msg['to']
    ticket_id = get_ticket_id(address)
    if ticket_id is not None:
        return Ticket(env, ticket_id)
    else:
        raise SystemExit("Could not find ticket ID in '%s'" % address)

def get_author(msg):
    """
    Determine the author of the comment.

    If 'trac@transparentnevada.com' is in the BCC field, I sent it so
    use my name.

    If 'trac@transparentnevada.com' is in the To field, I'm forwarding
    it from somebody else. Look for either 'By:' or 'From:' in the
    message body and use that.
    """
    if bcc_msg(msg):
        return 'Eric Davis'
    elif to_msg(msg):
        payload = msg.get_payload()
        match = re.search('(From|By): ?([^\n]+)', payload, re.I)
        if match:
            return match.group(2)
        else:
            return '(Unknown)'
    else:
        return '(Unknown)'

def get_comment(msg):
    """
    Return the comment to be appended to the ticket.
    """
    if bcc_msg(msg):
        return msg.get_payload()
    elif to_msg(msg):
        # emails addressed to trac via the 'To' header are always
        # plain text, so no need to check any of that.
        payload = msg.get_payload()
        return '\n\n'.join(payload.split('\n\n')[1:])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', help="path of Trac environment")
    args = parser.parse_args()

    msg = email.message_from_file(sys.stdin)
    env = open_environment(args.env)
    ticket = get_ticket(env, msg)

    if ticket is not None:
        author = get_author(msg)
        comment = get_comment(msg)
        if comment and author:
            ticket.save_changes(author, comment)
        else:
            raise SystemExit("Author and/or comment missing")
