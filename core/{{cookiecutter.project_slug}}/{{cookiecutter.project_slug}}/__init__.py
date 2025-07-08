# SPDX-License-Identifier: {{ cookiecutter.code_license }}
try:
	from importlib import metadata
	__version__ = metadata.version(__package__)
except Exception:
	__version__ = 'unknown'

__all__ = tuple[str]()
