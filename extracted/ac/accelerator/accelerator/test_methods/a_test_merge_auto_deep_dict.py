# -*- coding: utf-8 -*-
############################################################################
#                                                                          #
# Copyright (c) 2025 Carl Drougge                                          #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#  http://www.apache.org/licenses/LICENSE-2.0                              #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
#                                                                          #
############################################################################

options = dict(
	allow_overwrite=False,
	dups=False,
)

def analysis(sliceno):
	res = {
		'shared': {'per slice': {sliceno: 'a'}},
		sliceno: {'exclusive': {'sliceno': sliceno}},
	}
	if options.dups:
		res['shared']['in every slice'] = {'foo': 'bar'}
	return res

def synthesis(analysis_res, slices):
	got = analysis_res.merge_auto(allow_overwrite=options.allow_overwrite)
	want = {sliceno: {'exclusive': {'sliceno': sliceno}} for sliceno in range(slices)}
	want['shared'] = {'per slice': {sliceno: 'a' for sliceno in range(slices)}}
	if options.dups:
		want['shared']['in every slice'] = {'foo': 'bar'}
	assert got == want, "Wanted %r, got %r" % (want, got,)
