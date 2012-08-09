"""
trac_cop.py -- write tickets
"""

import re
import sys
import email
import argparse
from trac.ticket import Ticket
from trac.env import open_environment

START_MARKER = '-- begin'
END_MARKER = '-- end'

def get_ticket_id(address):
    """
    Get the ticket ID out of the address.
    """
    match = re.search('^trac\+(\d+)@', address)
    if match:
        return int(match.group(1))
    else:
        raise Exception("Could not find ticket ID in '%s'" % address)

def get_payload(msg):
    """
    Return the first text/plain payload.
    """
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            return part.get_payload()

def extract_meta_info(msg, key=None):
    """
    Extract metainfo from the payload.

    Format is:
    -- begin
    key: value
    key2: value
    -- end

    Look in 'test_emails/' for examples.

    Return a dictionary of those keys and values.
    """
    payload = get_payload(msg)
    in_meta = False
    values = {}
    for line in payload.split('\n'):
        if line.startswith(START_MARKER):
            in_meta = True
            continue
        if in_meta and re.search('^([^:]+): ?(.+)$', line):
            key, value = line.split(': ', 1)
            values[key] = value
            continue
        if line.startswith(END_MARKER):
            break

    return values or None

def get_ticket(env, msg):
    """
    Return the appropriate Trac ticket.
    """
    ticket_id = get_ticket_id(msg['delivered-to'])
    return Ticket(env, ticket_id)

def get_author(msg):
    """
    Determine the author of the comment.
    """
    # If where it was delivered is not where it was sent (i.e., it's a
    # BCC), use my name.
    if msg['delivered-to'] != msg['to']:
        return 'Eric Davis'
    # If it was sent directly to Trac, parse out the name.
    else:
        meta = extract_meta_info(msg)
        # Had a metainfo section but no 'Author' key
        if meta is not None:
            return meta.get('Author', '(no author given)')
        # Didn't have any metainfo
        else:
            return '(no metainfo given)'

def get_comment(msg):
    """
    Return the comment to be appended to the ticket.
    """
    payload = get_payload(msg)
    if '-- end' in payload:
        idx = payload.find(END_MARKER) + len('-- end\n\n')
        return payload[idx:].strip()
    else:
        return payload.strip()

def main():
    """
    Entry point for cop.py
    """
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
