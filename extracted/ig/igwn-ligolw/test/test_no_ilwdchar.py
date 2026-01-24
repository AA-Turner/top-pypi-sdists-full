from subprocess import run

import pytest

pytest.importorskip("pytest_snapshot")

input = """\
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE LIGO_LW SYSTEM "http://ldas-sw.ligo.caltech.edu/doc/ligolwAPI/html/ligolw_dtd.txt">
<LIGO_LW>
	<Table Name="process:table">
		<Column Name="process:comment" Type="lstring"/>
		<Column Name="process:cvs_entry_time" Type="int_4s"/>
		<Column Name="process:cvs_repository" Type="lstring"/>
		<Column Name="process:domain" Type="lstring"/>
		<Column Name="process:end_time" Type="int_4s"/>
		<Column Name="process:ifos" Type="lstring"/>
		<Column Name="process:is_online" Type="int_4s"/>
		<Column Name="process:jobid" Type="int_4s"/>
		<Column Name="process:node" Type="lstring"/>
		<Column Name="process:process_id" Type="ilwd:char"/>
		<Column Name="process:program" Type="lstring"/>
		<Column Name="process:start_time" Type="int_4s"/>
		<Column Name="process:unix_procid" Type="int_4s"/>
		<Column Name="process:username" Type="lstring"/>
		<Column Name="process:version" Type="lstring"/>
		<Stream Delimiter="," Name="process:table" Type="Local">
			,1234737815,,,,,0,0,"detchar","process:process_id:0","/usr/bin/ligolw_segment_query_dqsegdb",1284753877,3729659,"detchar","a1e5109f4893fd04cab4237827f62382ec61d50f"
		</Stream>
	</Table>
	<Table Name="process_params:table">
		<Column Name="process_params:param" Type="lstring"/>
		<Column Name="process_params:process_id" Type="ilwd:char"/>
		<Column Name="process_params:program" Type="lstring"/>
		<Column Name="process_params:type" Type="lstring"/>
		<Column Name="process_params:value" Type="lstring"/>
		<Stream Delimiter="," Name="process_params:table" Type="Local">
			"--query-segments","process:process_id:0","/usr/bin/ligolw_segment_query_dqsegdb",,,
			"--gps-start-time","process:process_id:0","/usr/bin/ligolw_segment_query_dqsegdb","lstring","1248000000",
			"--segment-url","process:process_id:0","/usr/bin/ligolw_segment_query_dqsegdb","lstring","http://segments-backup.ldas.cit",
			"--result-name","process:process_id:0","/usr/bin/ligolw_segment_query_dqsegdb","lstring","RESULT",
			"--include-segments","process:process_id:0","/usr/bin/ligolw_segment_query_dqsegdb","lstring","H1:DMT-ANALYSIS_READY:1",
			"--gps-end-time","process:process_id:0","/usr/bin/ligolw_segment_query_dqsegdb","lstring","1249000000"
		</Stream>
	</Table>
	<Table Name="segment_definer:table">
		<Column Name="segment_definer:comment" Type="lstring"/>
		<Column Name="segment_definer:ifos" Type="lstring"/>
		<Column Name="segment_definer:name" Type="lstring"/>
		<Column Name="segment_definer:process_id" Type="ilwd:char"/>
		<Column Name="segment_definer:segment_def_id" Type="ilwd:char"/>
		<Column Name="segment_definer:version" Type="int_4s"/>
		<Stream Delimiter="," Name="segment_definer:table" Type="Local">
			"","H1","DMT-ANALYSIS_READY","process:process_id:0","segment_definer:segment_def_id:0",1,
			"","H1","RESULT","process:process_id:0","segment_definer:segment_def_id:1",1
		</Stream>
	</Table>
	<Table Name="segment_summary:table">
		<Column Name="segment_summary:comment" Type="lstring"/>
		<Column Name="segment_summary:end_time" Type="int_4s"/>
		<Column Name="segment_summary:end_time_ns" Type="int_4s"/>
		<Column Name="segment_summary:process_id" Type="ilwd:char"/>
		<Column Name="segment_summary:segment_def_id" Type="ilwd:char"/>
		<Column Name="segment_summary:segment_sum_id" Type="ilwd:char"/>
		<Column Name="segment_summary:start_time" Type="int_4s"/>
		<Column Name="segment_summary:start_time_ns" Type="int_4s"/>
		<Stream Delimiter="," Name="segment_summary:table" Type="Local">
			"",1248547791,0,"process:process_id:0","segment_definer:segment_def_id:0","segment_summary:segment_sum_id:0",1248000000,0,
			"",1248548493,0,"process:process_id:0","segment_definer:segment_def_id:0","segment_summary:segment_sum_id:1",1248548492,0,
			"",1248548681,0,"process:process_id:0","segment_definer:segment_def_id:0","segment_summary:segment_sum_id:2",1248548680,0,
			"",1248548734,0,"process:process_id:0","segment_definer:segment_def_id:0","segment_summary:segment_sum_id:3",1248548733,0,
			"",1248548749,0,"process:process_id:0","segment_definer:segment_def_id:0","segment_summary:segment_sum_id:4",1248548748,0,
			"",1249000000,0,"process:process_id:0","segment_definer:segment_def_id:0","segment_summary:segment_sum_id:5",1248548752,0,
			"",1249000000,0,"process:process_id:0","segment_definer:segment_def_id:1","segment_summary:segment_sum_id:6",1248000000,0
		</Stream>
	</Table>
	<Table Name="segment:table">
		<Column Name="segment:end_time" Type="int_4s"/>
		<Column Name="segment:end_time_ns" Type="int_4s"/>
		<Column Name="segment:process_id" Type="ilwd:char"/>
		<Column Name="segment:segment_def_id" Type="ilwd:char"/>
		<Column Name="segment:segment_id" Type="ilwd:char"/>
		<Column Name="segment:start_time" Type="int_4s"/>
		<Column Name="segment:start_time_ns" Type="int_4s"/>
		<Stream Delimiter="," Name="segment:table" Type="Local">
			1248121395,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:0",1248112045,0,
			1248166475,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:1",1248132100,0,
			1248190589,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:2",1248174716,0,
			1248222436,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:3",1248200309,0,
			1248256986,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:4",1248226964,0,
			1248257701,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:5",1248257433,0,
			1248293662,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:6",1248257810,0,
			1248316297,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:7",1248301515,0,
			1248347147,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:8",1248324635,0,
			1248428216,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:9",1248357841,0,
			1248455993,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:10",1248435887,0,
			1248469308,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:11",1248463090,0,
			1248500422,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:12",1248473324,0,
			1248533198,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:13",1248508576,0,
			1248565673,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:14",1248564041,0,
			1248621977,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:15",1248580883,0,
			1248715847,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:16",1248683707,0,
			1248720749,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:17",1248718638,0,
			1248775749,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:18",1248736939,0,
			1248829996,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:19",1248797028,0,
			1248868674,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:20",1248830127,0,
			1248911714,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:21",1248876535,0,
			1248950084,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:22",1248911787,0,
			1248979951,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:23",1248959453,0,
			1249000000,0,"process:process_id:0","segment_definer:segment_def_id:1","segment:segment_id:24",1248980058,0
		</Stream>
	</Table>
</LIGO_LW>
"""


def test_no_ilwdchar(snapshot, tmp_path):
    filename = "test.xml"
    path = tmp_path / filename
    path.write_text(input)
    run(["igwn_ligolw_no_ilwdchar", path], check=True)
    snapshot.assert_match(path.read_bytes(), filename)
