#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Provides terminal printing functionality.
"""

__author__      = "Tsukumo"
__copyright__   = "Copyright 2014, Tsukumo"
__credits__     = [ ]
__license__     = "MIT"
__version__     = "0.0.1"
__maintainer__  = "Tsukumo"
__email__       = "tsukumo.da@gmail.com"
__status__      = "Development"


# python language imports
import os

class tcaps:
    """
    @brief termcaps provides terminal printing functionality.
    """


    # 'private' members

    # Defines the permissable colors for terminal output
    _colors = {
        'black'     :'0', #< ANSI modifiers
        'red'       :'1',
        'green'     :'2',
        'yellow'    :'3',
        'blue'      :'4',
        'magenta'   :'5',
        'cyan'      :'6',
        'white'     :'7',
        'default'   :'9'
    }


    # Defines the permissable attributes for terminal output
    _attribs = {
        'default'   :'0', #< ANSI modifiers
        'bold'      :'1',
        'dim'       :'2',
        'italic'    :'3',
        'underline' :'4',
        'blink'     :'5',
        'blink_fast':'6',
        'reverse'   :'7',
        'conceal'   :'8',
        'crossed'   :'9'
    }


    # Defines if color sets should return nothing
    # used to turn off styled printing for the entire project
    _styles = False


    # Defines the escape sequence used to send commands
    _escape = '\033['


    # 'public' functions

    def __init__(self, style):
        """
        @brief Creates a tcaps environment with the specified settings.

        @param[in] style Boolean whether styles should be displayed or not.
        """

        self._styles = style


    def styles_off(self):
        """
        @brief Turn off styled printing.

        This method will set the colors flag which will be checked
        when a start or end termcap is requested. If colors is set
        to false then nothing will be returned and therefore there
        will be no style on the resulting text.
        """

        self._styles = False


    def styles_on(self):
        """
        @brief Turn on styled printing.

        This method will set the colors flag which will be checked
        when a start or end termcap is requested. If colors is set
        to true then the normal termcaps will be returned and
        there will be style on the resulting text.
        """

        self._styles = True


    def start(self, fg=None, bg=None, attr=None):
        """
        @brief Starts a terminal style as specified

        @param[in] fg   Color to set the foreground to.
        @param[in] bg   Color to set the background to.
        @param[in] attr Style to set the attribute to.

        @return the string needed to start the specified terminal style
        """

        if not os.getenv('ANSI_COLORS_DISABLED') is None or not self._styles:
            return ''

        # Begin the string with the escape sequence
        holder = self._escape

        # If there is a foreground specified add it to the sequence
        if fg != None:
            holder += '3' + self._colors[fg] #< ANSI foreground starts with 3
            # If either of the others are defined add a semi-colon for formatting
            if bg != None or attr != None:
                holder += ';'

        # If there is a background specified add it to the sequence
        if bg != None:
            holder += '4' + self._colors[bg] #< ANSI background starts with 4
            # If there is also an attribute defined add a semi-color for formatting
            if attr != None:
                holder += ';'

        # If there is an attribute specified add it to the sequence
        if attr != None:
            holder += self._attribs[attr] #< ANSI attributes aren't prefixed

        # Add the modifier ending to the sequence
        holder += 'm'

        return holder


    def end(self, fg=False, bg=False, attr=None):
        """
        @brief Ends a terminal style as specified

        @param[in] fg   Color to set the foreground to.
        @param[in] bg   Color to set the background to.
        @param[in] attr Style to set the attribute to.

        @return the string needed to end the specified terminal style
        """
        if not os.getenv('ANSI_COLORS_DISABLED') is None or not self._styles:
            return ''

        # Begin the string with the escape sequence
        holder = self._escape

        # If foreground true remove it by writing the default foreground color
        if fg:
            holder += '3' + self._colors['default'] #< ANSI foreground starts with 3
            # If either of the others are defined add a semi-colon for formatting
            if bg or attr != None:
                holder += ';'

        # If background true remove it by writing the default background color
        if bg:
            holder += '4' + self._colors['default'] #< ANSI background starts with 4
            # If there is also an attribute defined add a semi-color for formatting
            if attr != None:
                holder += ';'

        # If there is an attribute specified add it to the sequence
        if attr != None:
            holder += '2' + self._attribs[attr]

        # Add the modifier ending to the sequence
        holder += 'm'

        return holder


    def default(self):
        """
        @brief Ends all terminal styles

        @return the string needed to set the terminal style to default
        """
        if not os.getenv('ANSI_COLORS_DISABLED') is None:
            return ''

        # Return the default ANSI sequence of 0
        return self._escape + '0m'


    def clear(self):
        """
        @brief Clears the terminal screen

        @return the string needed to clear the terminal screen
        """
        # Return the clear ANSI sequence of 2J
        return self._escape + '2J'


    def move_cursor(self, x, y):
        """
        @brief Moves the cursor to the given x,y

        @return the string needed to move the cursor to the specified position
        """
        # Return the make ANSI sequence
        return ''.join([self._escape, str(x), ';', str(y), 'H'])


    def reset_cursor(self):
        """
        @brief Resets the cursor to 0,0 on the screen

        @return the string needed to reset the cursor
        """
        # Return the blank cursor ANSI sequence of ;H
        return self._escape + ';H'


    def reset_screen(self):
        """
        @brief Clears the screen and resets the cursor to 0,0

        @return the string needed to clear the screen and reset the cursor
        """
        # Return the clear and blank cursor ANSI sequences of 2j and ;H
        return self._escape + '2J' + self._escape + ';H'
