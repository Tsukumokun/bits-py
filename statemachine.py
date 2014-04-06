#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
State Machine: implementation for python.
"""

__author__      = "Tsukumo"
__copyright__   = "Copyright 2014, Tsukumo"
__credits__     = [ ]
__license__     = "MIT"
__version__     = "0.0.1"
__maintainer__  = "Tsukumo"
__email__       = "tsukumo.da@gmail.com"
__status__      = "Development"

import types
import collections

class StateMachine:
    """
    @brief StateMachine implementation for python.

    Implements a state machine which may be created
    from a dictionary definition following this pattern:
    """

    ### State Machine
    ##
    # Generic state machine implementation
    #
    ## Initialization
    #
    #    {
    #        'initial': 'statename',
    #
    #        'transitions': [
    #
    #            { 'from': 'statename', 'on': [listofitems], 'to':'statename'},
    #            { 'from': 'statename', 'on': [listofitems], 'to':'statename'},
    #               NOTE: from must be specified
    #               NOTE: on may be an empty list (wildcard)
    #               NOTE: to defaults to the same as from
    #            etc..
    #
    #        ],
    #
    #        'callbacks': {
    #
    #            'enter': {
    #                'statename': callbackfunction,
    #                'statename': callbackfunction,
    #                etc..
    #            },
    #
    #            'leave': {
    #                'statename': callbackfunction,
    #                'statename': callbackfunction,
    #                etc..
    #            },
    #
    #            'stay':  {
    #                'statename': callbackfunction,
    #                'statename': callbackfunction,
    #                etc..
    #            }
    #
    #            'before': callbackfunction,
    #
    #            'after':  callbackfunction,
    #
    #            'error':  callbackfunction
    #        }
    #
    #    }
    #
    ## Callback precedence
    #
    #    callbacks[before]
    #    callbacks[error]               (if error)
    #    callbacks[stay][currentstate]  (if not changed and not error)
    #    callbacks[leave][currentstate] (if changed and not error)
    #    [transition]
    #    callbacks[enter][currentstate] (if changed and not error)
    #    callbacks[after]
    #
    ## Callback function
    #
    #    callback(event, from, to)
    #
    #    To cancel a transition return false from before or any leave
    #    state.
    #


    # 'private' members

    _settings = { }

    _current = ''


    # 'private' functions

    def _die(self, msg):
        raise Exception('StateMachine: ' + msg)


    def _get(self, item):
        """
        @brief Safely retrieves an item from settings
        """
        ret = self._settings.get(item[0])
        for level in item[1:]:
            if ret == None:
                break
            ret = ret.get(level)
        return ret


    def _verify(self):
        """
        @brief Verifies the settings of the current StateMachine
        """

        # Verify settings is a dictionary
        if not type(self._settings) is dict:
            self._die('settings must be a dictionary')

        # Verify transitions exists and is a list
        transitions = self._get(['transitions'])
        if not type(transitions) is list:
            self._die('transitions must be a list')

        # Verify all transitions are dictionaries with a valid from and on
        for transition in transitions:
            if not type(transition) is dict:
                self._die('transitions must be dictionaries')
            if not type(transition.get('from')) is str:
                self._die('transitions from must be a string')
            if not isinstance(transition.get('on'), collections.Iterable):
                self._die('transitions on must be iterable')
            if transition.get('to') != None:
                if not type(transition.get('to')) is str:
                    self._die('transitions to must be a string')

        # Verify initial exists and is a string
        if not type(self._get(['initial'])) is str:
            self._die('initial state must be a string')

        # Verify callbacks is set up properly
        callbacks = self._get(['callbacks'])
        if callbacks:
            if not type(callbacks) is dict:
                self._die('callbacks must be a dictionary')
            for items in callbacks:
                if not type(callbacks[items]) is dict:
                    if not isinstance(callbacks[items], types.FunctionType):
                        self._die('callback items must be dictionaries or functions')
                else:
                    for item in callbacks[items]:
                        if not isinstance( callbacks[items][item], types.FunctionType):
                            self._die('all callbacks must be functions')


    # 'public' functions

    def __init__(self, settings):
        """
        @brief Class initialization function stores and verifies
               passed settings.
        """

        self._settings = settings
        self._verify();
        self._current = self._get(['initial'])


    def step(self, item):
        """
        @brief Moves the state machine forward by one step.
        """

        # Default to and from
        fr = self._current
        to = None

        # Search for the next appropriate from item
        for items in self._get(['transitions']):
            if items['from'] == self._current:
                # If the transition is in on, or on is empty (wildcard)
                # set the to variable
                if not items['on'] or item in items['on']:
                    to = items.get('to') or self._current

        # Call error function if no transition existed
        if not to:
            error = self._get(['callbacks', 'error'])
            if error: error(fr, item, to)
            return

        # Invoke the generic before callback
        before = self._get(['callbacks', 'before'])
        if before:
            # Stop if returned false
            if before(fr, item, to) == False:
                return

        # If the transition moved invoke leaving callback
        if fr != to:
            leave = self._get(['callbacks', 'leave', self._current])
            if leave:
                # Stop if returned false
                if leave(fr, item, to) == False:
                    return
        # If the transition stayed invoke staying callback
        else:
            stay = self._get(['callbacks', 'stay', self._current])
            if stay: stay(fr, item, to)

        # Set the new current state
        self._current = to;

        # If the transition moved invoke entering callback
        if fr != to:
            enter = self._get(['callbacks', 'enter', self._current])
            if enter: enter(fr, item, to)

        # Invoke the generic after callback
        after = self._get(['callbacks', 'after'])
        if after: after(fr, item, to)
