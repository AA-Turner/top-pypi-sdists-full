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

from collections import Counter

options = dict(
	allow_overwrite=False,
)

def analysis(sliceno):
	return {sliceno, 'dup'}, Counter(a=sliceno, b=2)

def synthesis(analysis_res, slices):
	got_s, got_c = analysis_res.merge_auto(allow_overwrite=options.allow_overwrite)
	want_s = set(range(slices)) | {'dup'}
	want_c = Counter(a=sum(range(slices)), b=slices * 2)
	assert got_s == want_s, "Wanted set %r, got %r" % (want_s, got_s,)
	assert got_c == want_c, "Wanted Counter %r, got %r" % (want_c, got_c,)
