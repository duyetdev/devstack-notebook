# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf import settings
from django.template.defaultfilters import floatformat  # noqa
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon.utils import csvbase

from openstack_dashboard import api
from openstack_dashboard import usage

######################################
# import pandas as pd
# import numpy as np
# import re

# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt


# islab_log_path = getattr(settings, 'ROOT_PATH') + '/../../logs'
# with open(islab_log_path + '/horizon.log') as f:
#     islab_data = f.read()

# islab_data_line = islab_data.split('\n')
# islab_data_arr = []

# for i in range(len(islab_data_line)):
#     _group = re.match("([A-Z]+)\:", islab_data_line[i][27:])
#     if  _group and _group.group(1):
#         islab_data_arr.append({'date': islab_data_line[i][0:10], 'time': islab_data_line[i][11:19], 'type': _group.group(1), 'content': islab_data_line[i][27:], 'count': 1})
# islab_data_frame = pd.DataFrame(data=islab_data_arr)

# islab_data_frame_group = islab_data_frame.groupby(['date', 'type']).agg(np.sum)

# islab_data_frame_plot = islab_data_frame_group.unstack().plot(
#     kind='bar',
#     stacked=True,
#     layout=("Date", "Number"), 
#     figsize=(10, 5)
# )
# islab_data_frame_plot.legend(loc=1, borderaxespad=0.)

# fig = islab_data_frame_plot.get_figure()
# fig.savefig(getattr(settings, 'ROOT_PATH') + "/static/dashboard/img/horizon-admin-overview.png")

######################################


class GlobalUsageCsvRenderer(csvbase.BaseCsvResponse):

    columns = [_("Project Name"), _("VCPUs"), _("RAM (MB)"),
               _("Disk (GB)"), _("Usage (Hours)"), _("More")]

    def get_row_data(self):

        for u in self.context['usage'].usage_list:
            yield (u.project_name or u.tenant_id,
                   u.vcpus,
                   u.memory_mb,
                   u.local_gb,
                   floatformat(u.vcpu_hours, 2),
                   "x")


class GlobalOverview(usage.UsageView):
    table_class = usage.GlobalUsageTable
    usage_class = usage.GlobalUsage
    template_name = 'admin/overview/usage.html'
    csv_response_class = GlobalUsageCsvRenderer

    def get_context_data(self, **kwargs):
        context = super(GlobalOverview, self).get_context_data(**kwargs)
        context['monitoring'] = getattr(settings, 'EXTERNAL_MONITORING', [])
        return context

    def get_data(self):
        data = super(GlobalOverview, self).get_data()
        # Pre-fill project names
        try:
            projects, has_more = api.keystone.tenant_list(self.request)
        except Exception:
            projects = []
            exceptions.handle(self.request,
                              _('Unable to retrieve project list.'))
        for instance in data:
            project = filter(lambda t: t.id == instance.tenant_id, projects)
            # If we could not get the project name, show the tenant_id with
            # a 'Deleted' identifier instead.
            if project:
                instance.project_name = getattr(project[0], "name", None)
            else:
                deleted = _("Deleted")
                instance.project_name = translation.string_concat(
                    instance.tenant_id, " (", deleted, ")")
        return data

