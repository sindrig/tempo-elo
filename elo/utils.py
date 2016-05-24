from django.http import Http404

from .models import ECOSYSTEMS


def validate_ecosystem_exists(ecosystem):
    if ecosystem not in (ecosystem for ecosystem, name in ECOSYSTEMS):
        raise Http404('Ecosystem does not exist')
