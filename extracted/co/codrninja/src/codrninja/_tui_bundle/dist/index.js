#!/usr/bin/env node
import React from 'react';
import { render } from 'ink';
import { App } from './App.js';
// Disable mouse capture so native terminal text selection works
process.stdout.write('\x1b[?1000l\x1b[?1002l\x1b[?1003l');
render(React.createElement(App, null), { exitOnCtrlC: true });
