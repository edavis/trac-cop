from nose.tools import *
import email
import trac_cop

def open_email(path):
    return email.message_from_file(open(path))

def test_get_ticket_id():
    eq_(1, trac_cop.get_ticket_id('trac+1@transparentnevada.com'))
    eq_(10, trac_cop.get_ticket_id('trac+10@transparentnevada.com'))
    assert_raises(Exception, trac_cop.get_ticket_id, 'trac@transparentnevada.com')

def test_extract_meta_info():
    msg = open_email('test_emails/forward.eml')
    eq_({'Author': 'Kristi Boosman'}, trac_cop.extract_meta_info(msg))

    msg = open_email('test_emails/no_meta.eml')
    assert_is_none(trac_cop.extract_meta_info(msg))

def test_get_author():
    msg = open_email('test_emails/bcc.eml')
    eq_('Eric Davis', trac_cop.get_author(msg))

    msg = open_email('test_emails/forward.eml')
    eq_('Kristi Boosman', trac_cop.get_author(msg))

    msg = open_email('test_emails/no_meta.eml')
    eq_('(no metainfo given)', trac_cop.get_author(msg))

    msg = open_email('test_emails/has_meta_no_author.eml')
    eq_('(no author given)', trac_cop.get_author(msg))

def test_get_comment():
    msg = open_email('test_emails/no_meta.eml')
    eq_('no meta info here', trac_cop.get_comment(msg))

    msg = open_email('test_emails/forward.eml')
    eq_('Content here', trac_cop.get_comment(msg))
