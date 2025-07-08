#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# This script does any needed pre-gen setup, like
# configuration option validation.
#

import re

from pathlib    import Path
from subprocess import check_call, CalledProcessError

MODULE_NAME_REGEX   = re.compile(r'^[_a-zA-Z][\w\d_]+$')
MODULE_NAME_LITERAL = '{{ cookiecutter.project_slug }}'

def main() -> int:
	cwd = Path.cwd()

	if not MODULE_NAME_REGEX.match(MODULE_NAME_LITERAL):
		print(f'Error: Invalid Python module name \'{MODULE_NAME_LITERAL}\'')
		print('Python module names may not start with a number or contain any spaces or hyphens (-)')

		return 1

	if '{{ cookiecutter.initialize_vcs }}' in ('yes', 'y', 'on', 't', 'true', '1'):
		try:
			check_call(('git', 'init'), cwd = cwd)
		except CalledProcessError:
			pass

	return 0

if __name__ == '__main__':
	raise SystemExit(main())
