# -*- coding: utf-8 -*-
"""
Unified bootstrap for legacy API4 mod packs.

Why this exists:
- this pack has lots of modules with monkey-patches,
  but only a few are imported by default.
- we centralize module loading order here so patches are applied reliably.
"""

import os
import imp

try:
    import bs
except Exception:
    bs = None

_bootstrap_done = False
_loaded_modules = []


def _patch_effects_and_map(settings_mod):
    if bs is None:
        return

    # Particle/effect optimization: keep visuals similar while reducing cost.
    if _cfg(settings_mod, 'fxOptimize', True):
        try:
            if not hasattr(bs, '_orig_emitBGDynamics'):
                bs._orig_emitBGDynamics = bs.emitBGDynamics

            scale = float(_cfg(settings_mod, 'fxCountScale', 0.45))
            max_count = int(_cfg(settings_mod, 'fxCountMax', 120))

            def _emitBGDynamics_optimized(*args, **kwargs):
                cnt = kwargs.get('count', None)
                if cnt is not None:
                    try:
                        cnt_i = int(cnt)
                        cnt_i = int(max(1, min(max_count, round(cnt_i * scale))))
                        kwargs['count'] = cnt_i
                    except Exception:
                        pass
                return bs._orig_emitBGDynamics(*args, **kwargs)

            bs.emitBGDynamics = _emitBGDynamics_optimized
            _log('patched emitBGDynamics (scale=' + str(scale) + ', max=' + str(max_count) + ')')
        except Exception:
            _log('failed to patch emitBGDynamics')
            if hasattr(bs, 'printException'):
                bs.printException('fx optimization patch failed')

    # Map default scale tweak: scale terrain nodes only (players unaffected).
    try:
        map_scale = float(_cfg(settings_mod, 'mapScale', 1.0))
        if abs(map_scale - 1.0) > 0.001 and not hasattr(bs, '_orig_newNode_for_map_scale'):
            bs._orig_newNode_for_map_scale = bs.newNode

            def _newNode_scaled(*args, **kwargs):
                # Keep full compatibility with all call styles:
                #   bs.newNode('terrain', ...)
                #   bs.newNode(type='terrain', ...)
                # and even weird internal no-arg/error paths.
                nodeType = None
                if len(args) > 0:
                    nodeType = args[0]
                elif 'type' in kwargs:
                    nodeType = kwargs.get('type')

                if nodeType == 'terrain':
                    attrs = kwargs.get('attrs')
                    if isinstance(attrs, dict) and 'scale' in attrs:
                        s = attrs.get('scale', None)
                        try:
                            # only scale nodes that already define scale;
                            # do NOT inject new scale attr (unsupported on many terrain nodes)
                            if isinstance(s, (int, float)):
                                attrs['scale'] = s * map_scale
                            elif isinstance(s, (tuple, list)):
                                attrs['scale'] = tuple([v * map_scale for v in s])
                        except Exception:
                            pass

                return bs._orig_newNode_for_map_scale(*args, **kwargs)

            bs.newNode = _newNode_scaled
            _log('patched newNode terrain scale x' + str(map_scale))
    except Exception:
        _log('failed to patch map scale')
        if bs is not None and hasattr(bs, 'printException'):
            bs.printException('map scale patch failed')


def _log(msg):
    print '[mod_bootstrap] ' + str(msg)


def _safe_import(module_name):
    try:
        __import__(module_name)
        _loaded_modules.append(module_name)
        _log('loaded ' + module_name)
        return True
    except Exception:
        _log('failed to load ' + module_name)
        if bs is not None and hasattr(bs, 'printException'):
            try:
                bs.printException('mod bootstrap import error: ' + module_name)
            except Exception:
                pass
        return False


def _safe_import_file(alias, filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(path):
        _log('file not found: ' + filename)
        return False
    try:
        imp.load_source(alias, path)
        _loaded_modules.append(alias)
        _log('loaded ' + filename + ' as ' + alias)
        return True
    except Exception:
        _log('failed to load file: ' + filename)
        if bs is not None and hasattr(bs, 'printException'):
            try:
                bs.printException('mod bootstrap file import error: ' + filename)
            except Exception:
                pass
        return False


def _cfg(settings_mod, key, default):
    if settings_mod is None:
        return default
    return getattr(settings_mod, key, default)


def bootstrap():
    global _bootstrap_done
    if _bootstrap_done:
        return

    _bootstrap_done = True

    settings_mod = None
    try:
        import settings
        settings_mod = settings
    except Exception:
        settings_mod = None

    _patch_effects_and_map(settings_mod)

    # Order matters for monkey patches.
    if _cfg(settings_mod, 'bootstrap_spaz', True):
        _safe_import('spazPC')

    if _cfg(settings_mod, 'bootstrap_powerup', True):
        _safe_import('pcpowerup')

    if _cfg(settings_mod, 'bootstrap_bomb', True):
        _safe_import('newBomb')

    if _cfg(settings_mod, 'bootstrap_kill_lightning', True):
        _safe_import('kill_lightning_fx')

    if _cfg(settings_mod, 'bootstrap_impact_no_friendlyfire', True):
        _safe_import('impact_bomb_no_friendlyfire')

    # optional modules
    if _cfg(settings_mod, 'bootstrap_prefix_tag', False):
        # original filename contains '-', not importable as module name
        _safe_import_file('prefix_tag', 'prefix-tag.py')

    if _cfg(settings_mod, 'bootstrap_chat_filter', False):
        _safe_import('filter')

    _log('done. loaded: ' + ', '.join(_loaded_modules))


def get_loaded_modules():
    return list(_loaded_modules)
