import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from statemachine import StateMachine

callbacks = [ ]

def callback():
    pass

def before_callback(f, o, t):
    callbacks.append('before[f=' + str(f) + ';o=' + str(o) + ';t=' + str(t) + ']')

def leave_callback(f, o, t):
    callbacks.append('leave [f=' + str(f) + ';o=' + str(o) + ';t=' + str(t) + ']')

def stay_callback(f, o, t):
    callbacks.append('stay  [f=' + str(f) + ';o=' + str(o) + ';t=' + str(t) + ']')

def enter_callback(f, o, t):
    callbacks.append('enter [f=' + str(f) + ';o=' + str(o) + ';t=' + str(t) + ']')

def after_callback(f, o, t):
    callbacks.append('after [f=' + str(f) + ';o=' + str(o) + ';t=' + str(t) + ']')

def error_callback(f, o, t):
    callbacks.append('error [f=' + str(f) + ';o=' + str(o) + ';t=' + str(t) + ']')

def test_verify_settings_is_a_dictionary():
    try:
        machine = StateMachine(None)
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: settings must be a dictionary')

def test_verify_transitions_is_a_list():
    try:
        machine = StateMachine({ })
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: transitions must be a list')

def test_verify_transitions_are_dictionaries():
    try:
        machine = StateMachine({ 'transitions': [ 'thing' ] })
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: transitions must be dictionaries')

def test_verify_transitions_have_items():
    try:
        machine = StateMachine({ 'initial': [ ], 'transitions': [
            { }
        ] })
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: transitions from must be a string')

    try:
        machine = StateMachine({ 'initial': 'state', 'transitions': [
            { 'from': 'state' }
        ] })
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: transitions on must be iterable')

    try:
        machine = StateMachine({ 'initial': 'state', 'transitions': [
            { 'from': 'state', 'on': [ ], 'to': [ ] }
        ] })
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: transitions to must be a string')

def test_verify_sunny_day_transitions():
    try:
        machine = StateMachine({ 'initial': 'state', 'transitions': [
            { 'from': 'state', 'on': [ ], 'to': 'thing' }
        ] })
    except Exception as inst:
        assert(False)

def test_verify_initial_state_is_string():
    try:
        machine = StateMachine({ 'transitions': [ ] })
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: initial state must be a string')

    try:
        machine = StateMachine({ 'initial': [ ], 'transitions': [ ] })
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: initial state must be a string')

def test_verify_sunny_day_no_callbacks():
    try:
        machine = StateMachine({ 'initial': 'state', 'transitions': [ ] })
    except Exception as inst:
        assert(False)

def test_verify_callbacks_is_dictionary():
    try:
        machine = StateMachine({ 'initial': 'state', 'transitions': [ ],
            'callbacks': 3
        })
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: callbacks must be a dictionary')

def test_verify_callbacks_are_dictionaries():
    try:
        machine = StateMachine({ 'initial': 'state', 'transitions': [ ],
            'callbacks': { 'item': 3 }
        })
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: callback items must be dictionaries or functions')

def test_verify_callbacks_are_functions():
    try:
        machine = StateMachine({ 'initial': 'state', 'transitions': [ ],
            'callbacks': {
                'item': {
                    'other': 3
                }
            }
        })
        assert(False)
    except Exception as inst:
        assert(str(inst) == 'StateMachine: all callbacks must be functions')

def test_verify_sunny_day_with_callbacks():
    try:
        machine = StateMachine({ 'initial': 'state', 'transitions': [ ],
            'callbacks': {
                'item': {
                    'other': callback
                }
            }
        })
        assert(machine._current == 'state')
    except Exception as inst:
        assert(False)

def get_machine():
    return StateMachine({
        'initial'    : 'a',
        'transitions': [
            # A can only go to b on a 1
            { 'from': 'a', 'on': [1], 'to': 'b'},
            # Always stay on b without erroring
            { 'from': 'b', 'on': [ ] }
        ],
        'callbacks'  : {
            'before' : before_callback,
            'after'  : after_callback,
            'leave'  : {
                'a': leave_callback,
                'b': leave_callback
            },
            'enter'  : {
                'a': enter_callback,
                'b': enter_callback
            },
            'stay'   : {
                'a': stay_callback,
                'b': stay_callback
            },
            'error'  : error_callback
        }
    })

def test_step_sunny_day():
    global callbacks

    callbacks = [ ]
    machine = get_machine()
    machine.step(1)
    machine.step(1)
    assert(callbacks == ['before[f=a;o=1;t=b]',
                         'leave [f=a;o=1;t=b]',
                         'enter [f=a;o=1;t=b]',
                         'after [f=a;o=1;t=b]',
                         'before[f=b;o=1;t=b]',
                         'stay  [f=b;o=1;t=b]',
                         'after [f=b;o=1;t=b]'] )

def test_step_error():
    global callbacks

    callbacks = [ ]
    machine = get_machine()
    machine.step(2)
    assert(callbacks == ['error [f=a;o=2;t=None]'])

def test_weak_wildcard():
    machine = StateMachine({
        'initial'    : 'a',
        'transitions': [
            # A can only go to b on a 1
            { 'from': 'a', 'on': [1], 'to': 'b'},
            # Always stay on b without erroring
            { 'from': 'a', 'on': [ ] }
        ]
    })
    machine.step(1)
    assert(machine._current == 'b')
