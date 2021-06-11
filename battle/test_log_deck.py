import pygame
from log_deck import LogDeck


def test_log_init():
    pygame.font.init()
    log_deck = LogDeck()
    assert log_deck.log_list == []


def test_log_init_scroll_up():
    pygame.font.init()
    log_deck = LogDeck()
    log_deck.scroll_up()
    assert log_deck.bound == 0


def test_log_init_scroll_down():
    pygame.font.init()
    log_deck = LogDeck()
    log_deck.scroll_down()
    assert log_deck.bound == 0


def test_log_max_records_bound():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records):
        log_deck.add_record("Text")
    assert log_deck.bound == 0


def test_log_max_records_scroll_up():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records):
        log_deck.add_record("Text")
    log_deck.scroll_up()
    assert log_deck.bound == 0


def test_log_max_records_scroll_down():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records):
        log_deck.add_record("Text")
    log_deck.scroll_down()
    assert log_deck.bound == 0


def test_log_add_record():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records * 10):
        log_deck.add_record(f"Text{i}")
    assert log_deck.log_list == [f"Text{i}" for i in range(log_deck.max_records * 10)]


def test_log_bound():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records * 10):
        log_deck.add_record(f"Text{i}")
    assert log_deck.bound == 0


def test_log_bound_scroll_up_once():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records * 10):
        log_deck.add_record(f"Text{i}")
    log_deck.scroll_up()
    assert log_deck.bound == 1


def test_log_bound_scroll_up_full():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records * 10):
        log_deck.add_record(f"Text{i}")
    for _ in range(log_deck.max_records * 20):
        log_deck.scroll_up()
    assert log_deck.bound == len(log_deck.log_list) - log_deck.max_records


def test_log_bound_scroll_down():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records * 10):
        log_deck.add_record(f"Text{i}")
    for _ in range(log_deck.max_records * 20):
        log_deck.scroll_down()
    assert log_deck.bound == 0


def test_log_bound_scroll_mixed_return():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records * 10):
        log_deck.add_record(f"Text{i}")
    num_downs = log_deck.max_records
    num_ups = log_deck.max_records
    for _ in range(num_ups):
        log_deck.scroll_up()
    for _ in range(num_downs):
        log_deck.scroll_down()
    assert log_deck.bound == 0


def test_log_bound_scroll_mixed_return_reverse():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records * 10):
        log_deck.add_record(f"Text{i}")
    num_downs = log_deck.max_records
    num_ups = log_deck.max_records
    for _ in range(num_downs):
        log_deck.scroll_down()
    for _ in range(num_ups):
        log_deck.scroll_up()
    assert log_deck.bound == num_ups


def test_log_bound_scroll():
    pygame.font.init()
    log_deck = LogDeck()
    for i in range(log_deck.max_records * 10):
        log_deck.add_record(f"Text{i}")
    num_downs = log_deck.max_records
    num_ups = log_deck.max_records * 2
    for _ in range(num_ups):
        log_deck.scroll_up()
    for _ in range(num_downs):
        log_deck.scroll_down()
    assert log_deck.bound == log_deck.max_records
