#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
#
# This script extracts information from VCS to pre-populate
# some configuration fields for the templates.
#

import json

from pathlib    import Path
from subprocess import check_output, CalledProcessError

# A biased collection of default Licenses for code
DEFAULT_CODE_LICS = [
	'BSD-3-Clause',
	'0BSD',
	'Apache-2.0',
	'BSD-2-Clause',
	'MIT',
	'MPL-2.0',
	'CERN-OHL-P-2.0',
	'CERN-OHL-S-2.0',
	'CERN-OHL-W-2.0',
	'EUPL-1.2',
	'ISC',
	'Zlib',
	'CC0', # Effectively Public Domain:tm:
	'GPL-2.0-only',
	'GPL-2.0-or-later',
	'GPL-3.0-only',
	'GPL-3.0-or-later',
	'Other', # Escape Hatch
]

# A biased collection of default Licenses for documentation
DEFAULT_DOCS_LICS = [
	'Same As Code', # Sometimes the docs are under the same license as the code.
	'CC-BY-SA 4.0',
	'CC-BY-NC-SA 4.0',
	'CC-BY-NC 4.0',
	'CC-BY 4.0',
	'CC0', # Effectively Public Domain:tm:
	'GFDL-1.2-only',
	'GFDL-1.2-or-later',
	'GFDL-1.3-only',
	'GFDL-1.3-or-later',
	'Other', # Escape hatch
]

COOKIECUTTER_CONFIG = Path.cwd() / 'cookiecutter.json'

# This contains the common template params/defaults for the Torii templates
COOKIECUTTER_POLYFILL: dict[str, str] = {
	# Initial Project Details
	'project_name': '',
	'project_description': '',
	'project_slug': "{{ cookiecutter.project_name | lower | replace(' ', '_') }}",
	'package_name': "{{ cookiecutter.project_name | replace(' ', '-') }}",
	'min_python': [
		'3.11',
		'3.12',
		'3.13',
	],
	# Author Details
	'author': 'Yamada Hanako',
	'email': "{{ cookiecutter.author | lower | replace(' ', '.') }}@domain.tld",
	# VCS Details
	'forge': 'github.com',
	'forge_user': '',
	'initialize_vcs': 'y',
	# Ancillary Project Details
	'code_license': DEFAULT_CODE_LICS,
	'docs_license': DEFAULT_DOCS_LICS,
	# Package Details
	'pypi_username': '{{ cookiecutter.forge_user }}',

	# URLs generated from the given options
	'__spdx_url_code': 'https://spdx.org/licenses/{{ cookiecutter.code_license }}.html',
	'__spdx_url_docs': 'https://spdx.org/licenses/{{ cookiecutter.docs_license }}.html',
	'__forge_url': 'https://{{ cookiecutter.forge }}/{{ cookiecutter.forge_user }}/{{ cookiecutter.project_slug }}',
	'__pypi_url': 'https://pypi.org/project/{{ cookiecutter.package_name }}/',
	# Other overloadables
	'__extra_deps': []
}

def _get_git_cfg(value: str) -> None | str:
	try:
		return check_output(('git', 'config', 'get', value)).decode('utf-8').strip()
	except CalledProcessError:
		return None

def main() -> int:
	# Create a new base configuration
	base_config = COOKIECUTTER_POLYFILL.copy()

	# Populate the auto-populated fields
	if (author := _get_git_cfg('user.name')):
		base_config['author'] = author

	if (email := _get_git_cfg('user.email')):
		base_config['email'] = email

	# Ingest the base template config
	with COOKIECUTTER_CONFIG.open('r') as f:
		project_config = json.load(f)

	# Squish the two configs together, with the project config overloading our base
	base_config.update(project_config)

	# Re-write the base config with the new polyfills
	with COOKIECUTTER_CONFIG.open('w') as f:
		json.dump(base_config, f)

	return 0

if __name__ == '__main__':
	raise SystemExit(main())
