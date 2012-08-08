from nose.tools import *
import email
import trac_cop

def test_get_ticket_id():
    msg = email.message_from_string('To: trac+1@transparentnevada.com')
    eq_(1, trac_cop.get_ticket_id(msg))

def test_get_author():
    msg = email.message_from_string("To: trac+1@transparentnevada.com\n\nBy: Kristi Boosman\n\nmessage content here")
    eq_("Kristi Boosman", trac_cop.get_author(msg))

    msg = email.message_from_string("To: trac+1@transparentnevada.com\n\nFrom: Kristi Boosman\n\nmessage content here")
    eq_("Kristi Boosman", trac_cop.get_author(msg))

    msg = email.message_from_string("To: trac+1@transparentnevada.com\n\nmessage content here")
    eq_("(Unknown)", trac_cop.get_author(msg))

    msg = email.message_from_string("Bcc: trac+1@transparentnevada.com\n\nmessage content here")
    eq_("Eric Davis", trac_cop.get_author(msg))

def test_get_comment():
    msg = email.message_from_string("""To: trac+1@transparentnevada.com

From: Kristi Boosman

message content here

hello world""")
    eq_("message content here\n\nhello world", trac_cop.get_comment(msg))

    msg = email.message_from_string("""Bcc: trac+1@transparentnevada.com

hello world""")
    eq_("hello world", trac_cop.get_comment(msg))

