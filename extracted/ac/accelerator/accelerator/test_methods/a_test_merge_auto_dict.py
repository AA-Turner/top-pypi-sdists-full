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
	tupled=False,
)

def analysis(sliceno):
	res = {sliceno: str(sliceno)}
	if options.dups:
		res['dup'] = 'whee'
	if options.tupled:
		res = [sliceno], sliceno, res
	return res

def synthesis(analysis_res, slices):
	got = analysis_res.merge_auto(allow_overwrite=options.allow_overwrite)
	want = {sliceno: str(sliceno) for sliceno in range(slices)}
	if options.dups:
		want['dup'] = 'whee'
	if options.tupled:
		got = tuple(got)
		want = list(range(slices)), sum(range(slices)), want
	assert want == got, "Wanted %r, got %r" % (want, got,)
