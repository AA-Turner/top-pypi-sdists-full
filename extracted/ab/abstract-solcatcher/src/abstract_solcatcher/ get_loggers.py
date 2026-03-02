
texts = """2026-01-23T02:11:01.997926+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logIntake processed  3242707' }
2026-01-23T02:11:01.997944+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.997949+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:01.997953+00:00 abstractendeavors env[2992447]:   message: 'logIntake Sent  3242707 to logEntryQueue'
2026-01-23T02:11:01.997956+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.997965+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.997969+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:01.997973+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:01.997977+00:00 abstractendeavors env[2992447]:   details: { queue: 'logIntake', result: 3242707 }
2026-01-23T02:11:01.997981+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.997991+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry processed  3242495' }
2026-01-23T02:11:01.998000+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logIntake processed  3242712' }
2026-01-23T02:11:01.998010+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.998014+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.998018+00:00 abstractendeavors env[2992446]:   message: 'logEntry Sent  3242495 to txnEntryQueue'
2026-01-23T02:11:01.998021+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.998031+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.998036+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.998040+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:01.998045+00:00 abstractendeavors env[2992446]:   details: { queue: 'logEntry', result: 3242495 }
2026-01-23T02:11:01.998048+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.998055+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:01.998058+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:01.998061+00:00 abstractendeavors env[2992459]:   message: 'logIntake Sent  3242712 to logEntryQueue'
2026-01-23T02:11:01.998064+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:01.998067+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:01.998070+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:01.998074+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:01.998078+00:00 abstractendeavors env[2992459]:   details: { queue: 'logIntake', result: 3242712 }
2026-01-23T02:11:01.998081+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:01.998089+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logIntake processed  3242706' }
2026-01-23T02:11:01.998093+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.998097+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:01.998100+00:00 abstractendeavors env[2992447]:   message: 'logIntake Sent  3242706 to logEntryQueue'
2026-01-23T02:11:01.998104+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.998112+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logIntake processed  3242711' }
2026-01-23T02:11:01.998119+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.998122+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:01.998126+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:01.998129+00:00 abstractendeavors env[2992447]:   details: { queue: 'logIntake', result: 3242706 }
2026-01-23T02:11:01.998133+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.998140+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logIntake processed  3242713' }
2026-01-23T02:11:01.998144+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.998147+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.998150+00:00 abstractendeavors env[2992446]:   message: 'logIntake Sent  3242713 to logEntryQueue'
2026-01-23T02:11:01.998153+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.998160+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.998163+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.998167+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:01.998171+00:00 abstractendeavors env[2992446]:   details: { queue: 'logIntake', result: 3242713 }
2026-01-23T02:11:01.998174+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.998181+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:01.998185+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:01.998189+00:00 abstractendeavors env[2992458]:   message: 'logIntake Sent  3242711 to logEntryQueue'
2026-01-23T02:11:01.998193+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:01.998196+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:01.998200+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:01.998203+00:00 abstractendeavors env[2992458]:   message: 'Queue handler',
2026-01-23T02:11:01.998207+00:00 abstractendeavors env[2992458]:   details: { queue: 'logIntake', result: 3242711 }
2026-01-23T02:11:01.998210+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:01.998217+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry processed  3242500' }
2026-01-23T02:11:01.998529+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.998536+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.998540+00:00 abstractendeavors env[2992446]:   message: 'logEntry Sent  3242500 to txnEntryQueue'
2026-01-23T02:11:01.998544+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.998559+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.998569+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.998573+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:01.998577+00:00 abstractendeavors env[2992446]:   details: { queue: 'logEntry', result: 3242500 }
2026-01-23T02:11:01.998581+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.998597+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logEntry processed  3242565' }
2026-01-23T02:11:01.998602+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.998606+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:01.998609+00:00 abstractendeavors env[2992447]:   message: 'logEntry Sent  3242565 to txnEntryQueue'
2026-01-23T02:11:01.998613+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.998617+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.998621+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:01.998625+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:01.998629+00:00 abstractendeavors env[2992447]:   details: { queue: 'logEntry', result: 3242565 }
2026-01-23T02:11:01.998633+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.998637+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logIntake processed  3242709' }
2026-01-23T02:11:01.998643+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.998647+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:01.998653+00:00 abstractendeavors env[2992447]:   message: 'logIntake Sent  3242709 to logEntryQueue'
2026-01-23T02:11:01.998656+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.998660+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.998666+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:01.998669+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:01.998672+00:00 abstractendeavors env[2992447]:   details: { queue: 'logIntake', result: 3242709 }
2026-01-23T02:11:01.998678+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.998686+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:01.998690+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:01.998694+00:00 abstractendeavors env[2992459]:   message: 'pairData_',
2026-01-23T02:11:01.998698+00:00 abstractendeavors env[2992459]:   details: null,
2026-01-23T02:11:01.998701+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.998705+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:01.998709+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:01.998713+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:01.998716+00:00 abstractendeavors env[2992459]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:01.998720+00:00 abstractendeavors env[2992459]:   message: 'processMetaData',
2026-01-23T02:11:01.998724+00:00 abstractendeavors env[2992459]:   details: '558W6xyFbaqWj8dcM1mAuWtkiCqR8FYscmXFAxmFzxvE6cDh8DS1hi7vwWdrbTekNQMs6AmnqFoM38BwSsftnLno',
2026-01-23T02:11:01.998728+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.998732+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:01.998735+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:01.998738+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:01.998741+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:01.998747+00:00 abstractendeavors env[2992459]:   message: 'meta_id',
2026-01-23T02:11:01.998750+00:00 abstractendeavors env[2992459]:   details: 216873,
2026-01-23T02:11:01.998753+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.998756+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:01.998760+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:01.998770+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:01.998776+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:01.998779+00:00 abstractendeavors env[2992458]:   message: 'pairData_',
2026-01-23T02:11:01.998783+00:00 abstractendeavors env[2992458]:   details: null,
2026-01-23T02:11:01.998787+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.998790+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:01.998794+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:01.998798+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:01.998801+00:00 abstractendeavors env[2992458]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:01.998805+00:00 abstractendeavors env[2992458]:   message: 'processMetaData',
2026-01-23T02:11:01.998809+00:00 abstractendeavors env[2992458]:   details: '3nwWmpcKrwyiKB15Fj1jhdKrcB6K6XAMJERVQ3r9sHZjtasKWhDDE4LFkZnicq7Vst1aveznFCNZFDprHXpVPuap',
2026-01-23T02:11:01.998813+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.998817+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:01.998820+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:01.998824+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:01.998828+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:01.998832+00:00 abstractendeavors env[2992458]:   message: 'pairData_',
2026-01-23T02:11:01.998836+00:00 abstractendeavors env[2992458]:   details: null,
2026-01-23T02:11:01.998840+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.998844+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:01.998848+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:01.998852+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:01.998855+00:00 abstractendeavors env[2992458]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:01.998859+00:00 abstractendeavors env[2992458]:   message: 'processMetaData',
2026-01-23T02:11:01.998863+00:00 abstractendeavors env[2992458]:   details: 'Wsy8US9nQb4wwFa33eeN72jm3BKVh2G4U6UL6MBFrY8X8Fvx25vVFxsKzPwf9x7urH7XMnqTf82T8iTrdQnUEw9',
2026-01-23T02:11:01.998876+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.998888+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:01.998891+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:01.998894+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logEntry recieved  {"id":3242711}' }
2026-01-23T02:11:01.998906+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logIntake processed  3242710' }
2026-01-23T02:11:01.998909+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.998912+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:01.998915+00:00 abstractendeavors env[2992447]:   message: 'logIntake Sent  3242710 to logEntryQueue'
2026-01-23T02:11:01.998918+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.998921+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.998923+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:01.998926+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:01.998929+00:00 abstractendeavors env[2992447]:   details: { queue: 'logIntake', result: 3242710 }
2026-01-23T02:11:01.998932+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.998935+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logEntry recieved  {"id":3242712}' }
2026-01-23T02:11:01.998938+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.998941+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:01.998944+00:00 abstractendeavors env[2992447]:   message: 'meta_id',
2026-01-23T02:11:01.998947+00:00 abstractendeavors env[2992447]:   details: 217175,
2026-01-23T02:11:01.998950+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.998953+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:01.998956+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.998982+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.998988+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:01.998992+00:00 abstractendeavors env[2992446]:   message: 'Processing transaction logs',
2026-01-23T02:11:01.998996+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:01.999001+00:00 abstractendeavors env[2992446]:     signature: 'bVAzZubTdZhKgjXAh7W87zaKe2f2u8SK2cofxsZUSctkGw9U4S1xNLbsohjN694RkDmrizKuYhrcYttW29oeHQk',
2026-01-23T02:11:01.999005+00:00 abstractendeavors env[2992446]:     slot: 395279102
2026-01-23T02:11:01.999009+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:01.999013+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.999016+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:01.999020+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999029+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:01.999033+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:01.999037+00:00 abstractendeavors env[2992458]:   message: 'meta_id',
2026-01-23T02:11:01.999042+00:00 abstractendeavors env[2992458]:   details: 216873,
2026-01-23T02:11:01.999046+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.999050+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:01.999053+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:01.999062+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999066+00:00 abstractendeavors env[2992446]:   mint: '3vFfPaCQq8B43nXqFw6V5hpEH6bnHzyCbrT6hnBqpump',
2026-01-23T02:11:01.999080+00:00 abstractendeavors env[2992446]:   sol_amount: 97777776n,
2026-01-23T02:11:01.999089+00:00 abstractendeavors env[2992446]:   token_amount: 3485823952649n,
2026-01-23T02:11:01.999093+00:00 abstractendeavors env[2992446]:   is_buy: false,
2026-01-23T02:11:01.999096+00:00 abstractendeavors env[2992446]:   user: 'EakJFWecdbQnNLbRsD9ZGsHJdAVJzTQ9iLxoxNXjuX3x',
2026-01-23T02:11:01.999099+00:00 abstractendeavors env[2992446]:   timestamp: 1769121763n,
2026-01-23T02:11:01.999102+00:00 abstractendeavors env[2992446]:   virtual_sol_reserves: 30000000008n,
2026-01-23T02:11:01.999105+00:00 abstractendeavors env[2992446]:   virtual_token_reserves: 1073000000000000n,
2026-01-23T02:11:01.999109+00:00 abstractendeavors env[2992446]:   real_sol_reserves: 8n,
2026-01-23T02:11:01.999126+00:00 abstractendeavors env[2992446]:   real_token_reserves: 793100000000000n,
2026-01-23T02:11:01.999132+00:00 abstractendeavors env[2992446]:   fee_recipient: '7hTckgnGnLQR6sdH7YkqFTAA7VwTfYFaZ6EhEsU3saCX',
2026-01-23T02:11:01.999136+00:00 abstractendeavors env[2992446]:   fee_basis_points: 95n,
2026-01-23T02:11:01.999140+00:00 abstractendeavors env[2992446]:   fee: 928889n,
2026-01-23T02:11:01.999144+00:00 abstractendeavors env[2992446]:   creator: 'FAicXNV5FVqtfbpn4Zccs71XcfGeyxBSGbqLDyDJZjke',
2026-01-23T02:11:01.999148+00:00 abstractendeavors env[2992446]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:01.999152+00:00 abstractendeavors env[2992446]:   creator_fee: 293334n,
2026-01-23T02:11:01.999156+00:00 abstractendeavors env[2992446]:   track_volume: false,
2026-01-23T02:11:01.999159+00:00 abstractendeavors env[2992446]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:01.999163+00:00 abstractendeavors env[2992446]:   total_claimed_tokens: 0n,
2026-01-23T02:11:01.999167+00:00 abstractendeavors env[2992446]:   current_sol_volume: 0n,
2026-01-23T02:11:01.999171+00:00 abstractendeavors env[2992446]:   last_update_timestamp: 0n,
2026-01-23T02:11:01.999175+00:00 abstractendeavors env[2992446]:   ix_name: 'sell',
2026-01-23T02:11:01.999179+00:00 abstractendeavors env[2992446]:   mayhem_mode: false
2026-01-23T02:11:01.999182+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999186+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999190+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:01.999194+00:00 abstractendeavors env[2992446]:   message: 'decodedData',
2026-01-23T02:11:01.999198+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:01.999202+00:00 abstractendeavors env[2992446]:     mint: '3vFfPaCQq8B43nXqFw6V5hpEH6bnHzyCbrT6hnBqpump',
2026-01-23T02:11:01.999206+00:00 abstractendeavors env[2992446]:     sol_amount: 97777776n,
2026-01-23T02:11:01.999210+00:00 abstractendeavors env[2992446]:     token_amount: 3485823952649n,
2026-01-23T02:11:01.999213+00:00 abstractendeavors env[2992446]:     is_buy: false,
2026-01-23T02:11:01.999217+00:00 abstractendeavors env[2992446]:     user: 'EakJFWecdbQnNLbRsD9ZGsHJdAVJzTQ9iLxoxNXjuX3x',
2026-01-23T02:11:01.999221+00:00 abstractendeavors env[2992446]:     timestamp: 1769121763n,
2026-01-23T02:11:01.999225+00:00 abstractendeavors env[2992446]:     virtual_sol_reserves: 30000000008n,
2026-01-23T02:11:01.999229+00:00 abstractendeavors env[2992446]:     virtual_token_reserves: 1073000000000000n,
2026-01-23T02:11:01.999233+00:00 abstractendeavors env[2992446]:     real_sol_reserves: 8n,
2026-01-23T02:11:01.999237+00:00 abstractendeavors env[2992446]:     real_token_reserves: 793100000000000n,
2026-01-23T02:11:01.999240+00:00 abstractendeavors env[2992446]:     fee_recipient: '7hTckgnGnLQR6sdH7YkqFTAA7VwTfYFaZ6EhEsU3saCX',
2026-01-23T02:11:01.999244+00:00 abstractendeavors env[2992446]:     fee_basis_points: 95n,
2026-01-23T02:11:01.999248+00:00 abstractendeavors env[2992446]:     fee: 928889n,
2026-01-23T02:11:01.999253+00:00 abstractendeavors env[2992446]:     creator: 'FAicXNV5FVqtfbpn4Zccs71XcfGeyxBSGbqLDyDJZjke',
2026-01-23T02:11:01.999257+00:00 abstractendeavors env[2992446]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:01.999262+00:00 abstractendeavors env[2992446]:     creator_fee: 293334n,
2026-01-23T02:11:01.999266+00:00 abstractendeavors env[2992446]:     track_volume: false,
2026-01-23T02:11:01.999270+00:00 abstractendeavors env[2992446]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:01.999274+00:00 abstractendeavors env[2992446]:     total_claimed_tokens: 0n,
2026-01-23T02:11:01.999278+00:00 abstractendeavors env[2992446]:     current_sol_volume: 0n,
2026-01-23T02:11:01.999282+00:00 abstractendeavors env[2992446]:     last_update_timestamp: 0n,
2026-01-23T02:11:01.999286+00:00 abstractendeavors env[2992446]:     ix_name: 'sell',
2026-01-23T02:11:01.999290+00:00 abstractendeavors env[2992446]:     mayhem_mode: false
2026-01-23T02:11:01.999294+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:01.999299+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.999303+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:01.999307+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999322+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry processed  3242492' }
2026-01-23T02:11:01.999327+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999336+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.999349+00:00 abstractendeavors env[2992446]:   message: 'logEntry Sent  3242492 to txnEntryQueue'
2026-01-23T02:11:01.999366+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999370+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999374+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.999378+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:01.999382+00:00 abstractendeavors env[2992446]:   details: { queue: 'logEntry', result: 3242492 }
2026-01-23T02:11:01.999387+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999391+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry processed  3242486' }
2026-01-23T02:11:01.999394+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999398+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.999402+00:00 abstractendeavors env[2992446]:   message: 'logEntry Sent  3242486 to txnEntryQueue'
2026-01-23T02:11:01.999406+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999410+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999414+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.999422+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:01.999426+00:00 abstractendeavors env[2992446]:   details: { queue: 'logEntry', result: 3242486 }
2026-01-23T02:11:01.999430+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999434+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logIntake processed  3242708' }
2026-01-23T02:11:01.999445+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999449+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.999453+00:00 abstractendeavors env[2992446]:   message: 'logIntake Sent  3242708 to logEntryQueue'
2026-01-23T02:11:01.999457+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999461+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999465+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:01.999469+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:01.999473+00:00 abstractendeavors env[2992446]:   details: { queue: 'logIntake', result: 3242708 }
2026-01-23T02:11:01.999476+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999483+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry recieved  {"id":3242707}' }
2026-01-23T02:11:01.999630+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999634+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:01.999638+00:00 abstractendeavors env[2992446]:   message: 'Processing transaction logs',
2026-01-23T02:11:01.999642+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:01.999646+00:00 abstractendeavors env[2992446]:     signature: 'iYdQzXQAoLMaNE1t4ut8Vrd697mWXVnKhsD43W8s386rgNpdvJW6AEUuWix9Yw39h2BcCjYkzCt7SaXbWeQYY5V',
2026-01-23T02:11:01.999650+00:00 abstractendeavors env[2992446]:     slot: 395279093
2026-01-23T02:11:01.999653+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:01.999657+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.999663+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:01.999666+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999674+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:01.999678+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:01.999681+00:00 abstractendeavors env[2992447]:   message: 'meta_id',
2026-01-23T02:11:01.999685+00:00 abstractendeavors env[2992447]:   details: 217209,
2026-01-23T02:11:01.999689+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.999693+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:01.999697+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:01.999705+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999709+00:00 abstractendeavors env[2992446]:   mint: 'FgNuGY4us9F2hWWKan6vv1DFNEyEEvBHMcxcjUDXpump',
2026-01-23T02:11:01.999713+00:00 abstractendeavors env[2992446]:   sol_amount: 106268246n,
2026-01-23T02:11:01.999717+00:00 abstractendeavors env[2992446]:   token_amount: 942656249009n,
2026-01-23T02:11:01.999721+00:00 abstractendeavors env[2992446]:   is_buy: true,
2026-01-23T02:11:01.999724+00:00 abstractendeavors env[2992446]:   user: '4rTK8SPJMrXLP8sBNiQHbgX7pvwEVwsF4QTqg2wV79iH',
2026-01-23T02:11:01.999728+00:00 abstractendeavors env[2992446]:   timestamp: 1769121760n,
2026-01-23T02:11:01.999732+00:00 abstractendeavors env[2992446]:   virtual_sol_reserves: 60293241402n,
2026-01-23T02:11:01.999736+00:00 abstractendeavors env[2992446]:   virtual_token_reserves: 533890686754475n,
2026-01-23T02:11:01.999740+00:00 abstractendeavors env[2992446]:   real_sol_reserves: 30293241402n,
2026-01-23T02:11:01.999744+00:00 abstractendeavors env[2992446]:   real_token_reserves: 253990686754475n,
2026-01-23T02:11:01.999748+00:00 abstractendeavors env[2992446]:   fee_recipient: '7hTckgnGnLQR6sdH7YkqFTAA7VwTfYFaZ6EhEsU3saCX',
2026-01-23T02:11:01.999752+00:00 abstractendeavors env[2992446]:   fee_basis_points: 95n,
2026-01-23T02:11:01.999755+00:00 abstractendeavors env[2992446]:   fee: 1009549n,
2026-01-23T02:11:01.999760+00:00 abstractendeavors env[2992446]:   creator: '6HkWQYbHeTRXsu1SdRHWpaoMfhkvJT4F7sDE39LEtpJs',
2026-01-23T02:11:01.999764+00:00 abstractendeavors env[2992446]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:01.999768+00:00 abstractendeavors env[2992446]:   creator_fee: 318805n,
2026-01-23T02:11:01.999772+00:00 abstractendeavors env[2992446]:   track_volume: true,
2026-01-23T02:11:01.999776+00:00 abstractendeavors env[2992446]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:01.999780+00:00 abstractendeavors env[2992446]:   total_claimed_tokens: 0n,
2026-01-23T02:11:01.999784+00:00 abstractendeavors env[2992446]:   current_sol_volume: 0n,
2026-01-23T02:11:01.999788+00:00 abstractendeavors env[2992446]:   last_update_timestamp: 0n,
2026-01-23T02:11:01.999792+00:00 abstractendeavors env[2992446]:   ix_name: 'buy',
2026-01-23T02:11:01.999796+00:00 abstractendeavors env[2992446]:   mayhem_mode: false
2026-01-23T02:11:01.999799+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999811+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999817+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:01.999820+00:00 abstractendeavors env[2992446]:   message: 'decodedData',
2026-01-23T02:11:01.999825+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:01.999829+00:00 abstractendeavors env[2992446]:     mint: 'FgNuGY4us9F2hWWKan6vv1DFNEyEEvBHMcxcjUDXpump',
2026-01-23T02:11:01.999833+00:00 abstractendeavors env[2992446]:     sol_amount: 106268246n,
2026-01-23T02:11:01.999838+00:00 abstractendeavors env[2992446]:     token_amount: 942656249009n,
2026-01-23T02:11:01.999842+00:00 abstractendeavors env[2992446]:     is_buy: true,
2026-01-23T02:11:01.999847+00:00 abstractendeavors env[2992446]:     user: '4rTK8SPJMrXLP8sBNiQHbgX7pvwEVwsF4QTqg2wV79iH',
2026-01-23T02:11:01.999852+00:00 abstractendeavors env[2992446]:     timestamp: 1769121760n,
2026-01-23T02:11:01.999856+00:00 abstractendeavors env[2992446]:     virtual_sol_reserves: 60293241402n,
2026-01-23T02:11:01.999861+00:00 abstractendeavors env[2992446]:     virtual_token_reserves: 533890686754475n,
2026-01-23T02:11:01.999865+00:00 abstractendeavors env[2992446]:     real_sol_reserves: 30293241402n,
2026-01-23T02:11:01.999869+00:00 abstractendeavors env[2992446]:     real_token_reserves: 253990686754475n,
2026-01-23T02:11:01.999874+00:00 abstractendeavors env[2992446]:     fee_recipient: '7hTckgnGnLQR6sdH7YkqFTAA7VwTfYFaZ6EhEsU3saCX',
2026-01-23T02:11:01.999878+00:00 abstractendeavors env[2992446]:     fee_basis_points: 95n,
2026-01-23T02:11:01.999882+00:00 abstractendeavors env[2992446]:     fee: 1009549n,
2026-01-23T02:11:01.999885+00:00 abstractendeavors env[2992446]:     creator: '6HkWQYbHeTRXsu1SdRHWpaoMfhkvJT4F7sDE39LEtpJs',
2026-01-23T02:11:01.999889+00:00 abstractendeavors env[2992446]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:01.999893+00:00 abstractendeavors env[2992446]:     creator_fee: 318805n,
2026-01-23T02:11:01.999896+00:00 abstractendeavors env[2992446]:     track_volume: true,
2026-01-23T02:11:01.999900+00:00 abstractendeavors env[2992446]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:01.999905+00:00 abstractendeavors env[2992446]:     total_claimed_tokens: 0n,
2026-01-23T02:11:01.999909+00:00 abstractendeavors env[2992446]:     current_sol_volume: 0n,
2026-01-23T02:11:01.999913+00:00 abstractendeavors env[2992446]:     last_update_timestamp: 0n,
2026-01-23T02:11:01.999918+00:00 abstractendeavors env[2992446]:     ix_name: 'buy',
2026-01-23T02:11:01.999922+00:00 abstractendeavors env[2992446]:     mayhem_mode: false
2026-01-23T02:11:01.999927+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:01.999931+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.999936+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:01.999940+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999949+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999954+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:01.999958+00:00 abstractendeavors env[2992446]:   message: 'pairData_',
2026-01-23T02:11:01.999962+00:00 abstractendeavors env[2992446]:   details: null,
2026-01-23T02:11:01.999965+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.999969+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:01.999973+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:01.999976+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:01.999980+00:00 abstractendeavors env[2992446]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:01.999984+00:00 abstractendeavors env[2992446]:   message: 'processMetaData',
2026-01-23T02:11:01.999988+00:00 abstractendeavors env[2992446]:   details: 'DEaxkbfiS8S2RLrDhvPwvN3Ccm6PymnQjVHwoAHqeSLCFBBh2tp8uXg2vQD13ogoNEeSZEeJ5WmmRGt2zH4M89n',
2026-01-23T02:11:01.999991+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:01.999996+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:01.999999+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.000290+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.000293+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.000296+00:00 abstractendeavors env[2992446]:   message: 'meta_id',
2026-01-23T02:11:02.000298+00:00 abstractendeavors env[2992446]:   details: 216862,
2026-01-23T02:11:02.000301+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.000304+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.000307+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.000347+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.000352+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.000355+00:00 abstractendeavors env[2992459]:   message: 'meta_id',
2026-01-23T02:11:02.000360+00:00 abstractendeavors env[2992459]:   details: 216873,
2026-01-23T02:11:02.000364+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.000368+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.000372+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.000381+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.000385+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:02.000389+00:00 abstractendeavors env[2992447]:   message: 'meta_id',
2026-01-23T02:11:02.000393+00:00 abstractendeavors env[2992447]:   details: 468,
2026-01-23T02:11:02.000398+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.000402+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.000406+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.001343+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.001349+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.001352+00:00 abstractendeavors env[2992446]:   message: 'pairData_',
2026-01-23T02:11:02.001355+00:00 abstractendeavors env[2992446]:   details: null,
2026-01-23T02:11:02.001358+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.001361+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.001364+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.001374+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.001378+00:00 abstractendeavors env[2992446]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:02.001380+00:00 abstractendeavors env[2992446]:   message: 'processMetaData',
2026-01-23T02:11:02.001384+00:00 abstractendeavors env[2992446]:   details: 'Nn3nUYhtT6UMo1uptAXsA4LbqMHh7fatFFrL7pirP8hJ4eKW6FZQNpvHSjvEBPggo1ApaE2TdEUz1beYMdTKgAQ',
2026-01-23T02:11:02.001387+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.001390+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.001394+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.001573+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.001576+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.001579+00:00 abstractendeavors env[2992446]:   message: 'Error processing transaction log',
2026-01-23T02:11:02.001582+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.001585+00:00 abstractendeavors env[2992446]:     error: '"null value in column \\"user_address\\" of relation \\"transactions\\" violates not-null constraint"',
2026-01-23T02:11:02.001589+00:00 abstractendeavors env[2992446]:     invocation: {
2026-01-23T02:11:02.001592+00:00 abstractendeavors env[2992446]:       data: [Array],
2026-01-23T02:11:02.001596+00:00 abstractendeavors env[2992446]:       logs: [Array],
2026-01-23T02:11:02.001599+00:00 abstractendeavors env[2992446]:       depth: 1,
2026-01-23T02:11:02.001603+00:00 abstractendeavors env[2992446]:       compute: [Object],
2026-01-23T02:11:02.001606+00:00 abstractendeavors env[2992446]:       children: [Array],
2026-01-23T02:11:02.001609+00:00 abstractendeavors env[2992446]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.001612+00:00 abstractendeavors env[2992446]:       invocation_index: 3,
2026-01-23T02:11:02.001615+00:00 abstractendeavors env[2992446]:       reported_invocation: 2
2026-01-23T02:11:02.001618+00:00 abstractendeavors env[2992446]:     }
2026-01-23T02:11:02.001621+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:02.001624+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.001627+00:00 abstractendeavors env[2992446]:   logType: 'error'
2026-01-23T02:11:02.001629+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.001752+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.001755+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.001758+00:00 abstractendeavors env[2992459]:   message: 'meta_id',
2026-01-23T02:11:02.001761+00:00 abstractendeavors env[2992459]:   details: 217323,
2026-01-23T02:11:02.001764+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.001767+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.001769+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.001975+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.001980+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.001983+00:00 abstractendeavors env[2992446]:   message: 'Error processing transaction log',
2026-01-23T02:11:02.001987+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.001991+00:00 abstractendeavors env[2992446]:     error: '"null value in column \\"user_address\\" of relation \\"transactions\\" violates not-null constraint"',
2026-01-23T02:11:02.001995+00:00 abstractendeavors env[2992446]:     invocation: {
2026-01-23T02:11:02.001999+00:00 abstractendeavors env[2992446]:       data: [Array],
2026-01-23T02:11:02.002003+00:00 abstractendeavors env[2992446]:       logs: [Array],
2026-01-23T02:11:02.002006+00:00 abstractendeavors env[2992446]:       depth: 2,
2026-01-23T02:11:02.002010+00:00 abstractendeavors env[2992446]:       compute: [Object],
2026-01-23T02:11:02.002014+00:00 abstractendeavors env[2992446]:       children: [Array],
2026-01-23T02:11:02.002018+00:00 abstractendeavors env[2992446]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.002021+00:00 abstractendeavors env[2992446]:       invocation_index: 10,
2026-01-23T02:11:02.002026+00:00 abstractendeavors env[2992446]:       reported_invocation: 3
2026-01-23T02:11:02.002030+00:00 abstractendeavors env[2992446]:     }
2026-01-23T02:11:02.002033+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:02.002037+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.002041+00:00 abstractendeavors env[2992446]:   logType: 'error'
2026-01-23T02:11:02.002045+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.002357+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.002361+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.002365+00:00 abstractendeavors env[2992459]:   message: 'meta_id',
2026-01-23T02:11:02.002368+00:00 abstractendeavors env[2992459]:   details: 217302,
2026-01-23T02:11:02.002372+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.002375+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.002379+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.023991+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.023996+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.024007+00:00 abstractendeavors env[2992447]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"SCpNZaAkxe6Ea7MpGmZEaZhi1Aj8bksGMJKed5KuMxyNhaThNqMvh9gVpGMpYNuvfbcU7dFB8SRp8xhW9PxUGP9","slot":395310303,"logs_b64":"WyJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBDb21wdXRlQnVkZ2V0MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gRkxBU0hYOERyTGJnZVI4RmNmTlYxRjVrcnhZY1lNVWRCa3JQMUVQQnR4QjkgaW52b2tlIFsxXSIsIlByb2dyYW0gRjV0ZnZiTG9nOVZkR1VQcUJEVFQ4cmdYdlRUY3E3ZTVVaUdudXBMMXp2QnEgaW52b2tlIFsyXSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBpbnZva2UgWzNdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBHZXRGZWVzIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIGNvbnN1bWVkIDMxMjEgb2YgMTQzOTAwIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIHJldHVybjogcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBBQUFBQUFBQUFBQmZBQUFBQUFBQUFCNEFBQUFBQUFBQSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBzdWNjZXNzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGludm9rZSBbM10iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEJ1eSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBpbnZva2UgWzRdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBHZXRGZWVzIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIGNvbnN1bWVkIDMxMjEgb2YgOTg3NjcgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gcmV0dXJuOiBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIEFBQUFBQUFBQUFCZkFBQUFBQUFBQUI0QUFBQUFBQUFBIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIHN1Y2Nlc3MiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgaW52b2tlIFs0XSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogVHJhbnNmZXJDaGVja2VkIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGNvbnN1bWVkIDI0NzUgb2YgOTE4NDMgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzRdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzRdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzRdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBkYXRhOiB2ZHQvMDA3bVllNWVDMFlvRFF3QUYzTHpkek9idVdPclNXNFBNSmJrNnBhYVc0bDcyUnlMcnh3blV3a0FBQUFBZGtCQVBUc0JBQUFCbjlqT2hTZjhrWWUxMzBVNi9lUmFRdmw5cmtXSEFodU9tNitSR240OEZ6KzEySEpwQUFBQUFNRDh6RGNPQUFBQWtEekRvMjNmQVFEQVVLazdCd0FBQUpDa3NGZmM0QUFBalJnYURJU2ZxVGVtODByZTB3Z2UrVmNBcXNzTW03UFpDYVM1RkhVbnBPdGZBQUFBQUFBQUFJK3RGZ0FBQUFBQUxtTkd4VWlocjlIRDNnc2tEYWVkWVdndmkxUTRZM29KVU13Nnk4TjE5MlFlQUFBQUFBQUFBRllwQndBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUF3QUFBR0oxZVFBPSIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzRdIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDIwNTQgb2YgNzY3MDIgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDY0MTI0IG9mIDEzNzMzOCBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIHN1Y2Nlc3MiLCJQcm9ncmFtIEY1dGZ2YkxvZzlWZEdVUHFCRFRUOHJnWHZUVGNxN2U1VWlHbnVwTDF6dkJxIGNvbnN1bWVkIDcyNzM3IG9mIDE0NTgzNiBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSBGNXRmdmJMb2c5VmRHVVBxQkRUVDhyZ1h2VFRjcTdlNVVpR251cEwxenZCcSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzJdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBGTEFTSFg4RHJMYmdlUjhGY2ZOVjFGNWtyeFljWU1VZEJrclAxRVBCdHhCOSBjb25zdW1lZCA3ODU0OCBvZiAxNDk3MDAgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gRkxBU0hYOERyTGJnZVI4RmNmTlYxRjVrcnhZY1lNVWRCa3JQMUVQQnR4Qjkgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyJd"}'
2026-01-23T02:11:02.024011+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.024119+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logEntry recieved  {"id":3242709}' }
2026-01-23T02:11:02.024127+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry recieved  {"id":3242706}' }
2026-01-23T02:11:02.024145+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logEntry recieved  {"id":3242710}' }
2026-01-23T02:11:02.039625+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry recieved  {"id":3242708}' }
2026-01-23T02:11:02.039647+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry recieved  {"id":3242713}' }
2026-01-23T02:11:02.065332+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.065345+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.065359+00:00 abstractendeavors env[2992459]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"5YBGabFHpvboE34gzEKGAcR6wvtj6rTgLwbh5JjoQVduvvpf84JagukFadtwL1ByRcqGsaDxmf1RD2XAoh2EYGWQ","slot":395310303,"logs_b64":"WyJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBCWHhnR3QzYWtBZ2hadmlZSExoOEtVaDZ2aFhCaHQ1d2Y4NkRlNmh1VHA5NSBpbnZva2UgWzFdIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IFNlbGwiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogaW52b2tlIFszXSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogR2V0RmVlcyIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBjb25zdW1lZCAzMTIxIG9mIDk4NTY3IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIHJldHVybjogcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBBQUFBQUFBQUFBQmZBQUFBQUFBQUFCNEFBQUFBQUFBQSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBzdWNjZXNzIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbM10iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IFRyYW5zZmVyQ2hlY2tlZCIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCAyNDQ3IG9mIDkxNjgyIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgc3VjY2VzcyIsIlByb2dyYW0gZGF0YTogdmR0LzAwN21ZZTVlQzBZb0RRd0FGM0x6ZHpPYnVXT3JTVzRQTUpiazZwYWFXNGw3MlJ5THI4QlNlV3NBQUFBQWV3UmFSWllPQUFBQTZ4QTAxQnVJcTZuL29MVFBmZE9OWE5YTWprYm9nSmJRRWNUQ0FzUEh1cnExMkhKcEFBQUFBQUNxVTh3TkFBQUFDMEVkNlFQdUFRQUEvaS9RQmdBQUFBdXBDcDF5N3dBQVNzTDQwTjFjdkpmaktKd1pmTFVHS2xUejJWYTV6bTVSRmZsbFo2cGNzK1pmQUFBQUFBQUFBR2RnQlFFQUFBQUFMbU5HeFVpaHI5SEQzZ3NrRGFlZFlXZ3ZpMVE0WTNvSlVNdzZ5OE4xOTJRZUFBQUFBQUFBQUR5S1VnQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFCQUFBQUhObGJHd0EiLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgaW52b2tlIFszXSIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBjb25zdW1lZCAyMDU0IG9mIDgyNjI4IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBjb25zdW1lZCA0NzY0OCBvZiAxMjczMDcgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIiwiUHJvZ3JhbSBCWHhnR3QzYWtBZ2hadmlZSExoOEtVaDZ2aFhCaHQ1d2Y4NkRlNmh1VHA5NSBjb25zdW1lZCA1MDIwMiBvZiAxMjk4NTAgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gQlh4Z0d0M2FrQWdoWnZpWUhMaDhLVWg2dmhYQmh0NXdmODZEZTZodVRwOTUgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyJd"}'
2026-01-23T02:11:02.065365+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.065726+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.065735+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.065749+00:00 abstractendeavors env[2992458]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"4qUQRCSdz6Awu8y9VFaF2CXRKTXAqgqsM6HdZo4ZbLp6nP47i1W1xCnXWReviWrX38wJ32gqpynou1znF8ZwJix8","slot":395310303,"logs_b64":"WyJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBDb21wdXRlQnVkZ2V0MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzFdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBCdXkiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogaW52b2tlIFsyXSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogR2V0RmVlcyIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBjb25zdW1lZCAzMTIxIG9mIDU1NjA4IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIHJldHVybjogcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBBQUFBQUFBQUFBQmZBQUFBQUFBQUFCNEFBQUFBQUFBQSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBzdWNjZXNzIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IFRyYW5zZmVyQ2hlY2tlZCIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCAyNDc1IG9mIDQ4Njg0IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsyXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsyXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsyXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gZGF0YTogdmR0LzAwN21ZZTVlQzBZb0RRd0FGM0x6ZHpPYnVXT3JTVzRQTUpiazZwYWFXNGw3MlJ5THIrYnEwd0lBQUFBQXh1NndLV1VBQUFBQkdUd0RnS2RJTFVZNFFqOUZUZzdPaXNDaGEyZXlobWM1TmFqL3cxQmk4WUcxMkhKcEFBQUFBT2FVSjg4TkFBQUFSVkpzdjU3dEFRRG02QVBUQmdBQUFFVzZXWE1ON3dBQVNzTDQwTjFjdkpmaktKd1pmTFVHS2xUejJWYTV6bTVSRmZsbFo2cGNzK1pmQUFBQUFBQUFBSkxnQmdBQUFBQUFMbU5HeFVpaHI5SEQzZ3NrRGFlZFlXZ3ZpMVE0WTNvSlVNdzZ5OE4xOTJRZUFBQUFBQUFBQVBnckFnQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBd0FBQUdKMWVRQT0iLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgaW52b2tlIFsyXSIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBjb25zdW1lZCAyMDU0IG9mIDMzNTQzIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBjb25zdW1lZCA2MTA4MyBvZiA5MTEzOCBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIHN1Y2Nlc3MiLCJQcm9ncmFtIHRyb1kzNllpUEdxTXlBWUNOYkVxWUNkTjJ0YjkxWmY3YkhjUXQ3S1VpNjEgaW52b2tlIFsxXSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogRmVlVHJhbnNmZXIiLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMl0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiLCJQcm9ncmFtIHRyb1kzNllpUEdxTXlBWUNOYkVxWUNkTjJ0YjkxWmY3YkhjUXQ3S1VpNjEgY29uc3VtZWQgMzU2MCBvZiAzMDA1NSBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSB0cm9ZMzZZaVBHcU15QVlDTmJFcVlDZE4ydGI5MVpmN2JIY1F0N0tVaTYxIHN1Y2Nlc3MiXQ=="}'
2026-01-23T02:11:02.065754+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.107783+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.107795+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.107820+00:00 abstractendeavors env[2992447]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"3Emm7gX4QpXNeNLW372v7C5fTftieMyzHxPYVbQ8sbPLJzGLf87gB1rhF4f51Ljks7Gs2vQuhgHaQugNmSqVx7t4","slot":395310303,"logs_b64":"WyJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBDb21wdXRlQnVkZ2V0MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gQVRva2VuR1B2YmRHVnhyMWIyaHZaYnNpcVc1eFdIMjVlZlROc0xKQThrbkwgaW52b2tlIFsxXSIsIlByb2dyYW0gbG9nOiBDcmVhdGVJZGVtcG90ZW50IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEdldEFjY291bnREYXRhU2l6ZSIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCAxNDQ0IG9mIDEzNTkwMyBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSByZXR1cm46IFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgcWdBQUFBQUFBQUE9IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIHN1Y2Nlc3MiLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMl0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiLCJQcm9ncmFtIGxvZzogSW5pdGlhbGl6ZSB0aGUgYXNzb2NpYXRlZCB0b2tlbiBhY2NvdW50IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEluaXRpYWxpemVJbW11dGFibGVPd25lciIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCA2NzQgb2YgMTI5NTI5IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgc3VjY2VzcyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBpbnZva2UgWzJdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBJbml0aWFsaXplQWNjb3VudDMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgY29uc3VtZWQgMjAyNyBvZiAxMjY0NjcgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBzdWNjZXNzIiwiUHJvZ3JhbSBBVG9rZW5HUHZiZEdWeHIxYjJodlpic2lxVzV4V0gyNWVmVE5zTEpBOGtuTCBjb25zdW1lZCAxODU2NCBvZiAxNDI3MjEgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gQVRva2VuR1B2YmRHVnhyMWIyaHZaYnNpcVc1eFdIMjVlZlROc0xKQThrbkwgc3VjY2VzcyIsIlByb2dyYW0gR01nblZGUjhKYjM5TG9Yc0VWemIzRHZCeTN5d0NtZG1KcXVIVXkxTHJrcWIgaW52b2tlIFsxXSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogQnV5IiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEJ1eSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBpbnZva2UgWzNdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBHZXRGZWVzIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIGNvbnN1bWVkIDMxMjEgb2YgNjg4MDMgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gcmV0dXJuOiBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIEFBQUFBQUFBQUFCZkFBQUFBQUFBQUI0QUFBQUFBQUFBIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIHN1Y2Nlc3MiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgaW52b2tlIFszXSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogVHJhbnNmZXJDaGVja2VkIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGNvbnN1bWVkIDI0NzUgb2YgNjE4NzkgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzNdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzNdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzNdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBkYXRhOiB2ZHQvMDA3bVllNjMxcjJBL1N1b2dQN1V4NnljblIzOHg4MWZoWmxNa1pSZERyS1VGTTh3bnlMcjNRMEFBQUFBNmtlYS9Dd0RBQUFCakFCY3lLM1JNRzlMUldERUxLc2ZXYmNMdGl3NjVwTFJ2YnBjc1o3ZmZORzEySEpwQUFBQUFEbzFVYzhLQUFBQVVGN1ZSWlYyQWdBNmlTM1RBd0FBQUZER3d2a0RlQUVBMTZxUHNHRFlLUnRNVFVkZHIvZGl5V3ZjRGF6ck5zQVM2dEV1MDZsSVFXRmZBQUFBQUFBQUFHZTVJUUFBQUFBQTlNcUU2UGJwMWVrSUFxOERaZ0xjRG4zZGhPeUdhR2lWb2RZS0NYTnNuSThlQUFBQUFBQUFBRmVtQ2dBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUF3QUFBR0oxZVFBPSIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzNdIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDIwNTQgb2YgNDY3MzggY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDY1NjUyIG9mIDEwODkwMiBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIHN1Y2Nlc3MiLCJQcm9ncmFtIEdNZ25WRlI4SmIzOUxvWHNFVnpiM0R2QnkzeXdDbWRtSnF1SFV5MUxya3FiIGNvbnN1bWVkIDgyNjM4IG9mIDEyNDE1NyBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSBHTWduVkZSOEpiMzlMb1hzRVZ6YjNEdkJ5M3l3Q21kbUpxdUhVeTFMcmtxYiBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzFdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzFdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIl0="}'
2026-01-23T02:11:02.107827+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.107842+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.107848+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.107871+00:00 abstractendeavors env[2992446]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"4pcfxkLhjKik9DKYvr6LSVqc4snJuFHjZQqMvo8rswtNXxB97awNWSsGhK1kUTuqQGGmAarQ7Kcne9rQ8MdL4xWE","slot":395310303,"logs_b64":"WyJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBDb21wdXRlQnVkZ2V0MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gQVRva2VuR1B2YmRHVnhyMWIyaHZaYnNpcVc1eFdIMjVlZlROc0xKQThrbkwgaW52b2tlIFsxXSIsIlByb2dyYW0gbG9nOiBDcmVhdGVJZGVtcG90ZW50IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEdldEFjY291bnREYXRhU2l6ZSIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCAxNDQ0IG9mIDEzMjkwMyBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSByZXR1cm46IFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgcWdBQUFBQUFBQUE9IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIHN1Y2Nlc3MiLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMl0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiLCJQcm9ncmFtIGxvZzogSW5pdGlhbGl6ZSB0aGUgYXNzb2NpYXRlZCB0b2tlbiBhY2NvdW50IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEluaXRpYWxpemVJbW11dGFibGVPd25lciIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCA2NzQgb2YgMTI2NTI5IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgc3VjY2VzcyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBpbnZva2UgWzJdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBJbml0aWFsaXplQWNjb3VudDMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgY29uc3VtZWQgMjAyNyBvZiAxMjM0NjcgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBzdWNjZXNzIiwiUHJvZ3JhbSBBVG9rZW5HUHZiZEdWeHIxYjJodlpic2lxVzV4V0gyNWVmVE5zTEpBOGtuTCBjb25zdW1lZCAyMTU2NCBvZiAxNDI3MjEgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gQVRva2VuR1B2YmRHVnhyMWIyaHZaYnNpcVc1eFdIMjVlZlROc0xKQThrbkwgc3VjY2VzcyIsIlByb2dyYW0gR01nblZGUjhKYjM5TG9Yc0VWemIzRHZCeTN5d0NtZG1KcXVIVXkxTHJrcWIgaW52b2tlIFsxXSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogQnV5IiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEJ1eSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBpbnZva2UgWzNdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBHZXRGZWVzIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIGNvbnN1bWVkIDMxMjEgb2YgNjI3NzQgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gcmV0dXJuOiBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIEFBQUFBQUFBQUFCZkFBQUFBQUFBQUI0QUFBQUFBQUFBIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIHN1Y2Nlc3MiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgaW52b2tlIFszXSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogVHJhbnNmZXJDaGVja2VkIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGNvbnN1bWVkIDI0NzUgb2YgNTU4NTAgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzNdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzNdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzNdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBkYXRhOiB2ZHQvMDA3bVllNjMxcjJBL1N1b2dQN1V4NnljblIzOHg4MWZoWmxNa1pSZERyS1VGTTh3bjhqTEtRc0FBQUFBemlkK2xZZ0NBQUFCSk56L3o0TFpRMm8xRTRlVlFOdGxsdXA2TlhvcnZQVmlKRGFWNlFhbnkxZTEySEpwQUFBQUFBSUJlOW9LQUFBQWdqWlhzQXgwQWdBQ1ZWZmVBd0FBQUlLZVJHUjdkUUVBWUl6TUhmenBZYlE3ZDV3WkZRV200dE8vUmRXazIwWVlyWGJJTFdGMVJUVmZBQUFBQUFBQUFDa21Hd0FBQUFBQTlNcUU2UGJwMWVrSUFxOERaZ0xjRG4zZGhPeUdhR2lWb2RZS0NYTnNuSThlQUFBQUFBQUFBTXFTQ0FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUF3QUFBR0oxZVFBPSIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzNdIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDIwNTQgb2YgNDA3MDkgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDY4NjgxIG9mIDEwNTkwMiBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIHN1Y2Nlc3MiLCJQcm9ncmFtIEdNZ25WRlI4SmIzOUxvWHNFVnpiM0R2QnkzeXdDbWRtSnF1SFV5MUxya3FiIGNvbnN1bWVkIDg1NjY3IG9mIDEyMTE1NyBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSBHTWduVkZSOEpiMzlMb1hzRVZ6YjNEdkJ5M3l3Q21kbUpxdUhVeTFMcmtxYiBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzFdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzFdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIl0="}'
2026-01-23T02:11:02.107876+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.120438+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logEntry processed  3242566' }
2026-01-23T02:11:02.120576+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.120582+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.120586+00:00 abstractendeavors env[2992447]:   message: 'logEntry Sent  3242566 to txnEntryQueue'
2026-01-23T02:11:02.120589+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.120595+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.120598+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.120601+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:02.120604+00:00 abstractendeavors env[2992447]:   details: { queue: 'logEntry', result: 3242566 }
2026-01-23T02:11:02.120607+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.120614+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry processed  3242506' }
2026-01-23T02:11:02.120621+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logIntake processed  3242719' }
2026-01-23T02:11:02.120639+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.120644+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.120647+00:00 abstractendeavors env[2992446]:   message: 'logEntry Sent  3242506 to txnEntryQueue'
2026-01-23T02:11:02.120649+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.120656+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.120658+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.120661+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:02.120665+00:00 abstractendeavors env[2992446]:   details: { queue: 'logEntry', result: 3242506 }
2026-01-23T02:11:02.120668+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.120677+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logIntake processed  3242714' }
2026-01-23T02:11:02.120686+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.120690+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.120694+00:00 abstractendeavors env[2992459]:   message: 'logIntake Sent  3242719 to logEntryQueue'
2026-01-23T02:11:02.120698+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.120701+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.120705+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.120709+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.120716+00:00 abstractendeavors env[2992459]:   details: { queue: 'logIntake', result: 3242719 }
2026-01-23T02:11:02.120721+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.120729+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.120733+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.120737+00:00 abstractendeavors env[2992458]:   message: 'logIntake Sent  3242714 to logEntryQueue'
2026-01-23T02:11:02.120741+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.120744+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.120748+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.120752+00:00 abstractendeavors env[2992458]:   message: 'Queue handler',
2026-01-23T02:11:02.120756+00:00 abstractendeavors env[2992458]:   details: { queue: 'logIntake', result: 3242714 }
2026-01-23T02:11:02.120759+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.120766+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logIntake processed  3242716' }
2026-01-23T02:11:02.120772+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.120776+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.120779+00:00 abstractendeavors env[2992446]:   message: 'logIntake Sent  3242716 to logEntryQueue'
2026-01-23T02:11:02.120783+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.120790+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.120796+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.120799+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:02.120803+00:00 abstractendeavors env[2992446]:   details: { queue: 'logIntake', result: 3242716 }
2026-01-23T02:11:02.120807+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.120912+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logEntry processed  3242584' }
2026-01-23T02:11:02.120928+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.120936+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.120942+00:00 abstractendeavors env[2992458]:   message: 'logEntry Sent  3242584 to txnEntryQueue'
2026-01-23T02:11:02.120948+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.120960+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.120966+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.120972+00:00 abstractendeavors env[2992458]:   message: 'Queue handler',
2026-01-23T02:11:02.120979+00:00 abstractendeavors env[2992458]:   details: { queue: 'logEntry', result: 3242584 }
2026-01-23T02:11:02.120985+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.121002+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry processed  3242580' }
2026-01-23T02:11:02.121025+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.121032+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.121037+00:00 abstractendeavors env[2992459]:   message: 'logEntry Sent  3242580 to txnEntryQueue'
2026-01-23T02:11:02.121042+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.121053+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.121059+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.121064+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.121068+00:00 abstractendeavors env[2992459]:   details: { queue: 'logEntry', result: 3242580 }
2026-01-23T02:11:02.121072+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.121078+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logEntry recieved  {"id":3242714}' }
2026-01-23T02:11:02.121126+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logIntake processed  3242717' }
2026-01-23T02:11:02.121141+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.121145+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.121150+00:00 abstractendeavors env[2992459]:   message: 'logIntake Sent  3242717 to logEntryQueue'
2026-01-23T02:11:02.121154+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.121162+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.121166+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.121170+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.121174+00:00 abstractendeavors env[2992459]:   details: { queue: 'logIntake', result: 3242717 }
2026-01-23T02:11:02.121178+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.121186+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logEntry recieved  {"id":3242719}' }
2026-01-23T02:11:02.121223+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logIntake processed  3242718' }
2026-01-23T02:11:02.121243+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.121247+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.121251+00:00 abstractendeavors env[2992459]:   message: 'logIntake Sent  3242718 to logEntryQueue'
2026-01-23T02:11:02.121255+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.121261+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.121265+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.121268+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.121272+00:00 abstractendeavors env[2992459]:   details: { queue: 'logIntake', result: 3242718 }
2026-01-23T02:11:02.121276+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.121342+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logIntake processed  3242715' }
2026-01-23T02:11:02.121356+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.121361+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.121365+00:00 abstractendeavors env[2992459]:   message: 'logIntake Sent  3242715 to logEntryQueue'
2026-01-23T02:11:02.121369+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.121375+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.121381+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.121385+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.121389+00:00 abstractendeavors env[2992459]:   details: { queue: 'logIntake', result: 3242715 }
2026-01-23T02:11:02.121393+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.121446+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry processed  3242581' }
2026-01-23T02:11:02.121468+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.121471+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.121474+00:00 abstractendeavors env[2992459]:   message: 'logEntry Sent  3242581 to txnEntryQueue'
2026-01-23T02:11:02.121477+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.121482+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.121485+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.121488+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.121491+00:00 abstractendeavors env[2992459]:   details: { queue: 'logEntry', result: 3242581 }
2026-01-23T02:11:02.121494+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.121500+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.121503+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.121506+00:00 abstractendeavors env[2992446]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.121509+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.121512+00:00 abstractendeavors env[2992446]:     signature: '5xMpWqLu8p8hS3jbj2TcgEU6ao1GMvQdG6fBG7fGvBc1mnuxyfeGuE4zKM1Vy6swfjF3DWtEibVftH2QTdvWshxu',
2026-01-23T02:11:02.121515+00:00 abstractendeavors env[2992446]:     slot: 395279104
2026-01-23T02:11:02.121517+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:02.121520+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.121523+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.121526+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.121532+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.121535+00:00 abstractendeavors env[2992446]:   timestamp: 1769121764n,
2026-01-23T02:11:02.121538+00:00 abstractendeavors env[2992446]:   creator: '3Dtdhtjh8xaenuKtnkVCM5Ap7n6u9sXfwoEnWovdxhGW',
2026-01-23T02:11:02.121541+00:00 abstractendeavors env[2992446]:   creator_fee: 8328500n
2026-01-23T02:11:02.121544+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.121546+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.121549+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.121552+00:00 abstractendeavors env[2992446]:   message: 'decodedData',
2026-01-23T02:11:02.121556+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.121561+00:00 abstractendeavors env[2992446]:     timestamp: 1769121764n,
2026-01-23T02:11:02.121565+00:00 abstractendeavors env[2992446]:     creator: '3Dtdhtjh8xaenuKtnkVCM5Ap7n6u9sXfwoEnWovdxhGW',
2026-01-23T02:11:02.121569+00:00 abstractendeavors env[2992446]:     creator_fee: 8328500n
2026-01-23T02:11:02.121573+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:02.121577+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.121580+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.121584+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.121591+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.121596+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:02.121600+00:00 abstractendeavors env[2992447]:   message: 'meta_id',
2026-01-23T02:11:02.121604+00:00 abstractendeavors env[2992447]:   details: 217285,
2026-01-23T02:11:02.121608+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.121612+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.121617+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.121676+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.121680+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.121684+00:00 abstractendeavors env[2992446]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.121687+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.121691+00:00 abstractendeavors env[2992446]:     signature: '4CKkCdHq83AkLM4X95UG7CnPTPiCAj8vNjJLPhonnkmDPXhfoLHY1rbr52ik4RUR1cpMc6oc7vF6v8KeY62Gkjr6',
2026-01-23T02:11:02.121695+00:00 abstractendeavors env[2992446]:     slot: 395279092
2026-01-23T02:11:02.121698+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:02.121704+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.121707+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.121711+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.121738+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.121741+00:00 abstractendeavors env[2992446]:   mint: 'FGm8enpuyzhs9pck9xjbeiKtyfhdtDLrsNgpwaLBpump',
2026-01-23T02:11:02.121744+00:00 abstractendeavors env[2992446]:   sol_amount: 4938271n,
2026-01-23T02:11:02.121747+00:00 abstractendeavors env[2992446]:   token_amount: 169436748811n,
2026-01-23T02:11:02.121749+00:00 abstractendeavors env[2992446]:   is_buy: true,
2026-01-23T02:11:02.121753+00:00 abstractendeavors env[2992446]:   user: 'CbwxY1BBG71UFTSBYzavCXX3nAi73CTpDBaj4GqGUqYx',
2026-01-23T02:11:02.121756+00:00 abstractendeavors env[2992446]:   timestamp: 1769121760n,
2026-01-23T02:11:02.121759+00:00 abstractendeavors env[2992446]:   virtual_sol_reserves: 30632264877n,
2026-01-23T02:11:02.121762+00:00 abstractendeavors env[2992446]:   virtual_token_reserves: 1050852757119909n,
2026-01-23T02:11:02.121765+00:00 abstractendeavors env[2992446]:   real_sol_reserves: 632264877n,
2026-01-23T02:11:02.121768+00:00 abstractendeavors env[2992446]:   real_token_reserves: 770952757119909n,
2026-01-23T02:11:02.121772+00:00 abstractendeavors env[2992446]:   fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.121775+00:00 abstractendeavors env[2992446]:   fee_basis_points: 95n,
2026-01-23T02:11:02.121778+00:00 abstractendeavors env[2992446]:   fee: 46914n,
2026-01-23T02:11:02.121781+00:00 abstractendeavors env[2992446]:   creator: 'HkAEMTpSqASBBeWZPLczCFwJzniK8Y3w8eZtpv3n6B9W',
2026-01-23T02:11:02.121785+00:00 abstractendeavors env[2992446]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.121788+00:00 abstractendeavors env[2992446]:   creator_fee: 14815n,
2026-01-23T02:11:02.121792+00:00 abstractendeavors env[2992446]:   track_volume: false,
2026-01-23T02:11:02.121794+00:00 abstractendeavors env[2992446]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.121797+00:00 abstractendeavors env[2992446]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.121800+00:00 abstractendeavors env[2992446]:   current_sol_volume: 0n,
2026-01-23T02:11:02.121803+00:00 abstractendeavors env[2992446]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.121806+00:00 abstractendeavors env[2992446]:   ix_name: 'buy_exact_sol_in',
2026-01-23T02:11:02.121810+00:00 abstractendeavors env[2992446]:   mayhem_mode: false
2026-01-23T02:11:02.121812+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.121818+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.121821+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.121823+00:00 abstractendeavors env[2992446]:   message: 'decodedData',
2026-01-23T02:11:02.121826+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.121830+00:00 abstractendeavors env[2992446]:     mint: 'FGm8enpuyzhs9pck9xjbeiKtyfhdtDLrsNgpwaLBpump',
2026-01-23T02:11:02.121833+00:00 abstractendeavors env[2992446]:     sol_amount: 4938271n,
2026-01-23T02:11:02.121835+00:00 abstractendeavors env[2992446]:     token_amount: 169436748811n,
2026-01-23T02:11:02.121839+00:00 abstractendeavors env[2992446]:     is_buy: true,
2026-01-23T02:11:02.121842+00:00 abstractendeavors env[2992446]:     user: 'CbwxY1BBG71UFTSBYzavCXX3nAi73CTpDBaj4GqGUqYx',
2026-01-23T02:11:02.121845+00:00 abstractendeavors env[2992446]:     timestamp: 1769121760n,
2026-01-23T02:11:02.121847+00:00 abstractendeavors env[2992446]:     virtual_sol_reserves: 30632264877n,
2026-01-23T02:11:02.121850+00:00 abstractendeavors env[2992446]:     virtual_token_reserves: 1050852757119909n,
2026-01-23T02:11:02.121853+00:00 abstractendeavors env[2992446]:     real_sol_reserves: 632264877n,
2026-01-23T02:11:02.121856+00:00 abstractendeavors env[2992446]:     real_token_reserves: 770952757119909n,
2026-01-23T02:11:02.121858+00:00 abstractendeavors env[2992446]:     fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.121861+00:00 abstractendeavors env[2992446]:     fee_basis_points: 95n,
2026-01-23T02:11:02.121864+00:00 abstractendeavors env[2992446]:     fee: 46914n,
2026-01-23T02:11:02.121867+00:00 abstractendeavors env[2992446]:     creator: 'HkAEMTpSqASBBeWZPLczCFwJzniK8Y3w8eZtpv3n6B9W',
2026-01-23T02:11:02.121870+00:00 abstractendeavors env[2992446]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.121872+00:00 abstractendeavors env[2992446]:     creator_fee: 14815n,
2026-01-23T02:11:02.121875+00:00 abstractendeavors env[2992446]:     track_volume: false,
2026-01-23T02:11:02.121878+00:00 abstractendeavors env[2992446]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.121882+00:00 abstractendeavors env[2992446]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.121884+00:00 abstractendeavors env[2992446]:     current_sol_volume: 0n,
2026-01-23T02:11:02.121887+00:00 abstractendeavors env[2992446]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.121891+00:00 abstractendeavors env[2992446]:     ix_name: 'buy_exact_sol_in',
2026-01-23T02:11:02.121894+00:00 abstractendeavors env[2992446]:     mayhem_mode: false
2026-01-23T02:11:02.121896+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:02.121900+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.121903+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.121906+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.122787+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.122793+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:02.122798+00:00 abstractendeavors env[2992447]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.122802+00:00 abstractendeavors env[2992447]:   details: {
2026-01-23T02:11:02.122806+00:00 abstractendeavors env[2992447]:     signature: '5bqUJPM6gBEeMnKS463khdnh2FydDRQgLCk4PEXtQrm2WgfYsBxAzt1Mj67rwt2uCATPsymgxrd3RAojDjVnxALE',
2026-01-23T02:11:02.122810+00:00 abstractendeavors env[2992447]:     slot: 395279083
2026-01-23T02:11:02.122814+00:00 abstractendeavors env[2992447]:   },
2026-01-23T02:11:02.122818+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.122822+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.122826+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.122834+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.122839+00:00 abstractendeavors env[2992447]:   mint: '4BhxzE2ESP5jLzgGDRrpr5TGJ4TCiEC95wyJJUr9pump',
2026-01-23T02:11:02.122843+00:00 abstractendeavors env[2992447]:   sol_amount: 723900634n,
2026-01-23T02:11:02.122847+00:00 abstractendeavors env[2992447]:   token_amount: 21440467044928n,
2026-01-23T02:11:02.122851+00:00 abstractendeavors env[2992447]:   is_buy: false,
2026-01-23T02:11:02.122855+00:00 abstractendeavors env[2992447]:   user: '9c45Jw6zAEdt9RtnwW7VdBWJhgzM6ZsfFTF4bZjbRSfn',
2026-01-23T02:11:02.122859+00:00 abstractendeavors env[2992447]:   timestamp: 1769121756n,
2026-01-23T02:11:02.122863+00:00 abstractendeavors env[2992447]:   virtual_sol_reserves: 32607296055n,
2026-01-23T02:11:02.122867+00:00 abstractendeavors env[2992447]:   virtual_token_reserves: 987202373119175n,
2026-01-23T02:11:02.122871+00:00 abstractendeavors env[2992447]:   real_sol_reserves: 2607296055n,
2026-01-23T02:11:02.122875+00:00 abstractendeavors env[2992447]:   real_token_reserves: 707302373119175n,
2026-01-23T02:11:02.122879+00:00 abstractendeavors env[2992447]:   fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.122882+00:00 abstractendeavors env[2992447]:   fee_basis_points: 95n,
2026-01-23T02:11:02.122886+00:00 abstractendeavors env[2992447]:   fee: 6877057n,
2026-01-23T02:11:02.122890+00:00 abstractendeavors env[2992447]:   creator: 'HQnCWu39CZTQwHHmnuU4nSVAAd92cHFRfVV5NmoyDGLk',
2026-01-23T02:11:02.122894+00:00 abstractendeavors env[2992447]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.122899+00:00 abstractendeavors env[2992447]:   creator_fee: 2171702n,
2026-01-23T02:11:02.122903+00:00 abstractendeavors env[2992447]:   track_volume: false,
2026-01-23T02:11:02.122907+00:00 abstractendeavors env[2992447]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.122911+00:00 abstractendeavors env[2992447]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.122916+00:00 abstractendeavors env[2992447]:   current_sol_volume: 0n,
2026-01-23T02:11:02.122920+00:00 abstractendeavors env[2992447]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.122924+00:00 abstractendeavors env[2992447]:   ix_name: 'sell',
2026-01-23T02:11:02.122928+00:00 abstractendeavors env[2992447]:   mayhem_mode: false
2026-01-23T02:11:02.122932+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.122941+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.122945+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:02.122949+00:00 abstractendeavors env[2992458]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.122953+00:00 abstractendeavors env[2992458]:   details: {
2026-01-23T02:11:02.122958+00:00 abstractendeavors env[2992458]:     signature: '4NE5AfkAKjmzt2GDdsMqDqs9Q35jmD6yWM8NuKyzkdp5PauDNSCkPXCnRGaXfmRDeMg4ypn3oz5t1jtgB2dRk85f',
2026-01-23T02:11:02.122961+00:00 abstractendeavors env[2992458]:     slot: 395279104
2026-01-23T02:11:02.122965+00:00 abstractendeavors env[2992458]:   },
2026-01-23T02:11:02.122969+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.122973+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:02.122977+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.122981+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.122986+00:00 abstractendeavors env[2992458]:   mint: 'FunJWApfAEsCNY8SUsR8qv8mEyFjS8Lcht6MdXYRdX7A',
2026-01-23T02:11:02.122990+00:00 abstractendeavors env[2992458]:   sol_amount: 1000000n,
2026-01-23T02:11:02.122993+00:00 abstractendeavors env[2992458]:   token_amount: 34315060350n,
2026-01-23T02:11:02.122997+00:00 abstractendeavors env[2992458]:   is_buy: true,
2026-01-23T02:11:02.123001+00:00 abstractendeavors env[2992458]:   user: 'CgPxWeSa2JwwnGQeNECZY4D92gWgRqR9be41AiVsnCFR',
2026-01-23T02:11:02.123005+00:00 abstractendeavors env[2992458]:   timestamp: 1769121764n,
2026-01-23T02:11:02.123009+00:00 abstractendeavors env[2992458]:   virtual_sol_reserves: 30628462374n,
2026-01-23T02:11:02.123013+00:00 abstractendeavors env[2992458]:   virtual_token_reserves: 1050983219742711n,
2026-01-23T02:11:02.123016+00:00 abstractendeavors env[2992458]:   real_sol_reserves: 628462374n,
2026-01-23T02:11:02.123020+00:00 abstractendeavors env[2992458]:   real_token_reserves: 771083219742711n,
2026-01-23T02:11:02.123024+00:00 abstractendeavors env[2992458]:   fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.123028+00:00 abstractendeavors env[2992458]:   fee_basis_points: 95n,
2026-01-23T02:11:02.123032+00:00 abstractendeavors env[2992458]:   fee: 9500n,
2026-01-23T02:11:02.123037+00:00 abstractendeavors env[2992458]:   creator: '8Mw8NBU3NkA5N4EQT2gzyyqvciJ35477PhmBuRC2QR6T',
2026-01-23T02:11:02.123040+00:00 abstractendeavors env[2992458]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.123044+00:00 abstractendeavors env[2992458]:   creator_fee: 3000n,
2026-01-23T02:11:02.123048+00:00 abstractendeavors env[2992458]:   track_volume: false,
2026-01-23T02:11:02.123052+00:00 abstractendeavors env[2992458]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.123055+00:00 abstractendeavors env[2992458]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.123059+00:00 abstractendeavors env[2992458]:   current_sol_volume: 0n,
2026-01-23T02:11:02.123063+00:00 abstractendeavors env[2992458]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.123067+00:00 abstractendeavors env[2992458]:   ix_name: 'buy',
2026-01-23T02:11:02.123071+00:00 abstractendeavors env[2992458]:   mayhem_mode: false
2026-01-23T02:11:02.123075+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.123078+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.123082+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:02.123086+00:00 abstractendeavors env[2992458]:   message: 'decodedData',
2026-01-23T02:11:02.123091+00:00 abstractendeavors env[2992458]:   details: {
2026-01-23T02:11:02.123095+00:00 abstractendeavors env[2992458]:     mint: 'FunJWApfAEsCNY8SUsR8qv8mEyFjS8Lcht6MdXYRdX7A',
2026-01-23T02:11:02.123099+00:00 abstractendeavors env[2992458]:     sol_amount: 1000000n,
2026-01-23T02:11:02.123102+00:00 abstractendeavors env[2992458]:     token_amount: 34315060350n,
2026-01-23T02:11:02.123107+00:00 abstractendeavors env[2992458]:     is_buy: true,
2026-01-23T02:11:02.123111+00:00 abstractendeavors env[2992458]:     user: 'CgPxWeSa2JwwnGQeNECZY4D92gWgRqR9be41AiVsnCFR',
2026-01-23T02:11:02.123115+00:00 abstractendeavors env[2992458]:     timestamp: 1769121764n,
2026-01-23T02:11:02.123119+00:00 abstractendeavors env[2992458]:     virtual_sol_reserves: 30628462374n,
2026-01-23T02:11:02.123123+00:00 abstractendeavors env[2992458]:     virtual_token_reserves: 1050983219742711n,
2026-01-23T02:11:02.123127+00:00 abstractendeavors env[2992458]:     real_sol_reserves: 628462374n,
2026-01-23T02:11:02.123131+00:00 abstractendeavors env[2992458]:     real_token_reserves: 771083219742711n,
2026-01-23T02:11:02.123136+00:00 abstractendeavors env[2992458]:     fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.123139+00:00 abstractendeavors env[2992458]:     fee_basis_points: 95n,
2026-01-23T02:11:02.123143+00:00 abstractendeavors env[2992458]:     fee: 9500n,
2026-01-23T02:11:02.123147+00:00 abstractendeavors env[2992458]:     creator: '8Mw8NBU3NkA5N4EQT2gzyyqvciJ35477PhmBuRC2QR6T',
2026-01-23T02:11:02.123151+00:00 abstractendeavors env[2992458]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.123154+00:00 abstractendeavors env[2992458]:     creator_fee: 3000n,
2026-01-23T02:11:02.123158+00:00 abstractendeavors env[2992458]:     track_volume: false,
2026-01-23T02:11:02.123162+00:00 abstractendeavors env[2992458]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.123165+00:00 abstractendeavors env[2992458]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.123169+00:00 abstractendeavors env[2992458]:     current_sol_volume: 0n,
2026-01-23T02:11:02.123173+00:00 abstractendeavors env[2992458]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.123176+00:00 abstractendeavors env[2992458]:     ix_name: 'buy',
2026-01-23T02:11:02.123180+00:00 abstractendeavors env[2992458]:     mayhem_mode: false
2026-01-23T02:11:02.123184+00:00 abstractendeavors env[2992458]:   },
2026-01-23T02:11:02.123188+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.123193+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:02.123196+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.123205+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.123209+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:02.123213+00:00 abstractendeavors env[2992447]:   message: 'decodedData',
2026-01-23T02:11:02.123216+00:00 abstractendeavors env[2992447]:   details: {
2026-01-23T02:11:02.123221+00:00 abstractendeavors env[2992447]:     mint: '4BhxzE2ESP5jLzgGDRrpr5TGJ4TCiEC95wyJJUr9pump',
2026-01-23T02:11:02.123225+00:00 abstractendeavors env[2992447]:     sol_amount: 723900634n,
2026-01-23T02:11:02.123229+00:00 abstractendeavors env[2992447]:     token_amount: 21440467044928n,
2026-01-23T02:11:02.123233+00:00 abstractendeavors env[2992447]:     is_buy: false,
2026-01-23T02:11:02.123236+00:00 abstractendeavors env[2992447]:     user: '9c45Jw6zAEdt9RtnwW7VdBWJhgzM6ZsfFTF4bZjbRSfn',
2026-01-23T02:11:02.123240+00:00 abstractendeavors env[2992447]:     timestamp: 1769121756n,
2026-01-23T02:11:02.123244+00:00 abstractendeavors env[2992447]:     virtual_sol_reserves: 32607296055n,
2026-01-23T02:11:02.123247+00:00 abstractendeavors env[2992447]:     virtual_token_reserves: 987202373119175n,
2026-01-23T02:11:02.123251+00:00 abstractendeavors env[2992447]:     real_sol_reserves: 2607296055n,
2026-01-23T02:11:02.123256+00:00 abstractendeavors env[2992447]:     real_token_reserves: 707302373119175n,
2026-01-23T02:11:02.123260+00:00 abstractendeavors env[2992447]:     fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.123265+00:00 abstractendeavors env[2992447]:     fee_basis_points: 95n,
2026-01-23T02:11:02.123269+00:00 abstractendeavors env[2992447]:     fee: 6877057n,
2026-01-23T02:11:02.123274+00:00 abstractendeavors env[2992447]:     creator: 'HQnCWu39CZTQwHHmnuU4nSVAAd92cHFRfVV5NmoyDGLk',
2026-01-23T02:11:02.123277+00:00 abstractendeavors env[2992447]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.123281+00:00 abstractendeavors env[2992447]:     creator_fee: 2171702n,
2026-01-23T02:11:02.123285+00:00 abstractendeavors env[2992447]:     track_volume: false,
2026-01-23T02:11:02.123288+00:00 abstractendeavors env[2992447]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.123292+00:00 abstractendeavors env[2992447]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.123296+00:00 abstractendeavors env[2992447]:     current_sol_volume: 0n,
2026-01-23T02:11:02.123300+00:00 abstractendeavors env[2992447]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.123303+00:00 abstractendeavors env[2992447]:     ix_name: 'sell',
2026-01-23T02:11:02.123308+00:00 abstractendeavors env[2992447]:     mayhem_mode: false
2026-01-23T02:11:02.123312+00:00 abstractendeavors env[2992447]:   },
2026-01-23T02:11:02.123317+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.123321+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.123325+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.123353+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.123357+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.123361+00:00 abstractendeavors env[2992459]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.123365+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.123368+00:00 abstractendeavors env[2992459]:     signature: '5LRKUnEn35d7NhPXjMEwzv5cuVAF14vx76yeUNsSBDGgMJD9RyWWsuUjNmtX7V8ZRec7DF5yuxXauuGLCe2QdikW',
2026-01-23T02:11:02.123372+00:00 abstractendeavors env[2992459]:     slot: 395279104
2026-01-23T02:11:02.123376+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.123380+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.123384+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.123387+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.123392+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.123396+00:00 abstractendeavors env[2992459]:   mint: 'DmZVKmL9qhunaCv9f33U67L5sge14ktYjtvbMG9UH4FA',
2026-01-23T02:11:02.123401+00:00 abstractendeavors env[2992459]:   sol_amount: 98543731n,
2026-01-23T02:11:02.123404+00:00 abstractendeavors env[2992459]:   token_amount: 1034553448249n,
2026-01-23T02:11:02.123408+00:00 abstractendeavors env[2992459]:   is_buy: true,
2026-01-23T02:11:02.123412+00:00 abstractendeavors env[2992459]:   user: 'FDEoDAsB6UVwD5tY4LvoneAzP4gQuwx7g3Ym7FexSUpQ',
2026-01-23T02:11:02.123417+00:00 abstractendeavors env[2992459]:   timestamp: 1769121764n,
2026-01-23T02:11:02.123421+00:00 abstractendeavors env[2992459]:   virtual_sol_reserves: 55422353706n,
2026-01-23T02:11:02.123426+00:00 abstractendeavors env[2992459]:   virtual_token_reserves: 580812577310891n,
2026-01-23T02:11:02.123429+00:00 abstractendeavors env[2992459]:   real_sol_reserves: 25422353706n,
2026-01-23T02:11:02.123433+00:00 abstractendeavors env[2992459]:   real_token_reserves: 300912577310891n,
2026-01-23T02:11:02.123437+00:00 abstractendeavors env[2992459]:   fee_recipient: '7hTckgnGnLQR6sdH7YkqFTAA7VwTfYFaZ6EhEsU3saCX',
2026-01-23T02:11:02.123440+00:00 abstractendeavors env[2992459]:   fee_basis_points: 95n,
2026-01-23T02:11:02.123444+00:00 abstractendeavors env[2992459]:   fee: 936166n,
2026-01-23T02:11:02.123448+00:00 abstractendeavors env[2992459]:   creator: 'bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa',
2026-01-23T02:11:02.123453+00:00 abstractendeavors env[2992459]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.123457+00:00 abstractendeavors env[2992459]:   creator_fee: 295632n,
2026-01-23T02:11:02.123461+00:00 abstractendeavors env[2992459]:   track_volume: false,
2026-01-23T02:11:02.123465+00:00 abstractendeavors env[2992459]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.123469+00:00 abstractendeavors env[2992459]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.123473+00:00 abstractendeavors env[2992459]:   current_sol_volume: 0n,
2026-01-23T02:11:02.123478+00:00 abstractendeavors env[2992459]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.123482+00:00 abstractendeavors env[2992459]:   ix_name: 'buy',
2026-01-23T02:11:02.123486+00:00 abstractendeavors env[2992459]:   mayhem_mode: false
2026-01-23T02:11:02.123489+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.123493+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.123497+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.123501+00:00 abstractendeavors env[2992459]:   message: 'decodedData',
2026-01-23T02:11:02.123505+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.123509+00:00 abstractendeavors env[2992459]:     mint: 'DmZVKmL9qhunaCv9f33U67L5sge14ktYjtvbMG9UH4FA',
2026-01-23T02:11:02.123512+00:00 abstractendeavors env[2992459]:     sol_amount: 98543731n,
2026-01-23T02:11:02.123516+00:00 abstractendeavors env[2992459]:     token_amount: 1034553448249n,
2026-01-23T02:11:02.123520+00:00 abstractendeavors env[2992459]:     is_buy: true,
2026-01-23T02:11:02.123524+00:00 abstractendeavors env[2992459]:     user: 'FDEoDAsB6UVwD5tY4LvoneAzP4gQuwx7g3Ym7FexSUpQ',
2026-01-23T02:11:02.123528+00:00 abstractendeavors env[2992459]:     timestamp: 1769121764n,
2026-01-23T02:11:02.123532+00:00 abstractendeavors env[2992459]:     virtual_sol_reserves: 55422353706n,
2026-01-23T02:11:02.123536+00:00 abstractendeavors env[2992459]:     virtual_token_reserves: 580812577310891n,
2026-01-23T02:11:02.123541+00:00 abstractendeavors env[2992459]:     real_sol_reserves: 25422353706n,
2026-01-23T02:11:02.123545+00:00 abstractendeavors env[2992459]:     real_token_reserves: 300912577310891n,
2026-01-23T02:11:02.123549+00:00 abstractendeavors env[2992459]:     fee_recipient: '7hTckgnGnLQR6sdH7YkqFTAA7VwTfYFaZ6EhEsU3saCX',
2026-01-23T02:11:02.123553+00:00 abstractendeavors env[2992459]:     fee_basis_points: 95n,
2026-01-23T02:11:02.123557+00:00 abstractendeavors env[2992459]:     fee: 936166n,
2026-01-23T02:11:02.123561+00:00 abstractendeavors env[2992459]:     creator: 'bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa',
2026-01-23T02:11:02.123564+00:00 abstractendeavors env[2992459]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.123568+00:00 abstractendeavors env[2992459]:     creator_fee: 295632n,
2026-01-23T02:11:02.123572+00:00 abstractendeavors env[2992459]:     track_volume: false,
2026-01-23T02:11:02.123576+00:00 abstractendeavors env[2992459]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.123579+00:00 abstractendeavors env[2992459]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.123583+00:00 abstractendeavors env[2992459]:     current_sol_volume: 0n,
2026-01-23T02:11:02.123587+00:00 abstractendeavors env[2992459]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.123590+00:00 abstractendeavors env[2992459]:     ix_name: 'buy',
2026-01-23T02:11:02.123594+00:00 abstractendeavors env[2992459]:     mayhem_mode: false
2026-01-23T02:11:02.123598+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.123602+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.123606+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.123610+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.123619+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.123623+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:02.123626+00:00 abstractendeavors env[2992458]:   message: 'meta_id',
2026-01-23T02:11:02.123630+00:00 abstractendeavors env[2992458]:   details: 217285,
2026-01-23T02:11:02.123634+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.123638+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:02.123641+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.123965+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.123969+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:02.123973+00:00 abstractendeavors env[2992458]:   message: 'Error processing transaction log',
2026-01-23T02:11:02.123977+00:00 abstractendeavors env[2992458]:   details: {
2026-01-23T02:11:02.123981+00:00 abstractendeavors env[2992458]:     error: '"null value in column \\"user_address\\" of relation \\"transactions\\" violates not-null constraint"',
2026-01-23T02:11:02.123985+00:00 abstractendeavors env[2992458]:     invocation: {
2026-01-23T02:11:02.123989+00:00 abstractendeavors env[2992458]:       data: [Array],
2026-01-23T02:11:02.123992+00:00 abstractendeavors env[2992458]:       logs: [Array],
2026-01-23T02:11:02.123997+00:00 abstractendeavors env[2992458]:       depth: 1,
2026-01-23T02:11:02.124001+00:00 abstractendeavors env[2992458]:       compute: [Object],
2026-01-23T02:11:02.124005+00:00 abstractendeavors env[2992458]:       children: [Array],
2026-01-23T02:11:02.124010+00:00 abstractendeavors env[2992458]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.124013+00:00 abstractendeavors env[2992458]:       invocation_index: 8,
2026-01-23T02:11:02.124017+00:00 abstractendeavors env[2992458]:       reported_invocation: 2
2026-01-23T02:11:02.124021+00:00 abstractendeavors env[2992458]:     }
2026-01-23T02:11:02.124024+00:00 abstractendeavors env[2992458]:   },
2026-01-23T02:11:02.124029+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.124032+00:00 abstractendeavors env[2992458]:   logType: 'error'
2026-01-23T02:11:02.124037+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.148587+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.148597+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.148618+00:00 abstractendeavors env[2992459]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"2tF1X1ATUrXKChpxZcsAsPRT844r2n6ENEhExexwqTjwaKgQrNeQDTr9dq2PQwV2KcR7DsT91gh5Jfqu92r4Z71W","slot":395310303,"logs_b64":"WyJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBDb21wdXRlQnVkZ2V0MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gdGVybTlZUGI5bXpBc0FCYXFONzFBNHhkYnhIbXBCTlphdnBCaVFLWnpOMyBpbnZva2UgWzFdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBWYWxpZGF0ZU5vbmNlIiwiUHJvZ3JhbSB0ZXJtOVlQYjltekFzQUJhcU43MUE0eGRieEhtcEJOWmF2cEJpUUtaek4zIGNvbnN1bWVkIDMzMzkgb2YgMTc5NzAwIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIHRlcm05WVBiOW16QXNBQmFxTjcxQTR4ZGJ4SG1wQk5aYXZwQmlRS1p6TjMgc3VjY2VzcyIsIlByb2dyYW0gdGVybTlZUGI5bXpBc0FCYXFONzFBNHhkYnhIbXBCTlphdnBCaVFLWnpOMyBpbnZva2UgWzFdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBTZWxsRXhhY3RPdXRQdW1wRnVuIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IFNlbGwiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogaW52b2tlIFszXSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogR2V0RmVlcyIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBjb25zdW1lZCAzMTIxIG9mIDEzNTExNCBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSByZXR1cm46IHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogQUFBQUFBQUFBQUJmQUFBQUFBQUFBQjRBQUFBQUFBQUEiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogc3VjY2VzcyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBpbnZva2UgWzNdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBUcmFuc2ZlckNoZWNrZWQiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgY29uc3VtZWQgMjQ3NSBvZiAxMjgyMjkgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBzdWNjZXNzIiwiUHJvZ3JhbSBkYXRhOiB2ZHQvMDA3bVllNzQzREVOdGxyeDFjZnphTVVjbzd4VU5jeExvOGwrUThYODNXSHBrM29EbjVsUkxSNEFBQUFBOTdHdzk2TUNBQUFBdUVGUXJ0bW1YdGR2dmpkVGJjaTlSWllkdFB5RStNbmRYRzdUUWFDTGxCeTEySEpwQUFBQUFNRFRzMklSQUFBQW05NzFCQlNJQVFEQUo1Qm1DZ0FBQUp0RzQ3aUNpUUFBU3NMNDBOMWN2SmZqS0p3WmZMVUdLbFR6MlZhNXptNVJGZmxsWjZwY3MrWmZBQUFBQUFBQUFQcGpTUUFBQUFBQS9zRW1jSSttWWl4VTRXblRFbCtobk9iSzQ4MXlBZ1gwaEp1TXZxLzdQb2tlQUFBQUFBQUFBQXd0RndBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUJBQUFBSE5sYkd3QSIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzNdIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDIwNTQgb2YgMTE5MTQ3IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBjb25zdW1lZCA0OTE3NiBvZiAxNjUzNTQgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIiwiUHJvZ3JhbSB0ZXJtOVlQYjltekFzQUJhcU43MUE0eGRieEhtcEJOWmF2cEJpUUtaek4zIGNvbnN1bWVkIDYwODMxIG9mIDE3NjM2MSBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSB0ZXJtOVlQYjltekFzQUJhcU43MUE0eGRieEhtcEJOWmF2cEJpUUtaek4zIHN1Y2Nlc3MiLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiXQ=="}'
2026-01-23T02:11:02.148626+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.148756+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry recieved  {"id":3242718}' }
2026-01-23T02:11:02.148772+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry recieved  {"id":3242717}' }
2026-01-23T02:11:02.148787+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logEntry recieved  {"id":3242715}' }
2026-01-23T02:11:02.148862+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logEntry recieved  {"id":3242716}' }
2026-01-23T02:11:02.149045+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.149051+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.149074+00:00 abstractendeavors env[2992458]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"JtdbiF88SuVd9Z77PaNg9LQyRuNBXri9NNuAyNRtUs3B2VKy9zKy1A7Aju9UztMuKzpSs9wBdMZELcxeNEbYMdq","slot":395310303,"logs_b64":"WyJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBDb21wdXRlQnVkZ2V0MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gQVRva2VuR1B2YmRHVnhyMWIyaHZaYnNpcVc1eFdIMjVlZlROc0xKQThrbkwgaW52b2tlIFsxXSIsIlByb2dyYW0gbG9nOiBDcmVhdGVJZGVtcG90ZW50IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEdldEFjY291bnREYXRhU2l6ZSIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCAxNDQ0IG9mIDExNDIzMiBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSByZXR1cm46IFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgcWdBQUFBQUFBQUE9IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIHN1Y2Nlc3MiLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMl0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiLCJQcm9ncmFtIGxvZzogSW5pdGlhbGl6ZSB0aGUgYXNzb2NpYXRlZCB0b2tlbiBhY2NvdW50IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEluaXRpYWxpemVJbW11dGFibGVPd25lciIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCA2NzQgb2YgMTA3ODU4IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgc3VjY2VzcyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBpbnZva2UgWzJdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBJbml0aWFsaXplQWNjb3VudDMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgY29uc3VtZWQgMjAyNyBvZiAxMDQ3OTYgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBzdWNjZXNzIiwiUHJvZ3JhbSBBVG9rZW5HUHZiZEdWeHIxYjJodlpic2lxVzV4V0gyNWVmVE5zTEpBOGtuTCBjb25zdW1lZCAxNzA2NCBvZiAxMTk1NTAgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gQVRva2VuR1B2YmRHVnhyMWIyaHZaYnNpcVc1eFdIMjVlZlROc0xKQThrbkwgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzFdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBCdXkiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogaW52b2tlIFsyXSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogR2V0RmVlcyIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBjb25zdW1lZCAzMTIxIG9mIDYwODYxIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIHJldHVybjogcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBBQUFBQUFBQUFBQmZBQUFBQUFBQUFCNEFBQUFBQUFBQSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBzdWNjZXNzIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IFRyYW5zZmVyQ2hlY2tlZCIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCAyNDc1IG9mIDUzOTM3IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsyXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsyXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsyXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gZGF0YTogdmR0LzAwN21ZZTVwc1RTVWJRM1I0dzF3SjN2dmVXR0NmSnd2QUhyVXUxenE3UVhnclNNLzcrd0o4UUFBQUFBQVorY0NDaFlBQUFBQjBYSDh3SkM2VFhVNHJOTEJFeTF4ZlNDQk4wRVowS3VuWUNyTDZTdFc1aEsxMkhKcEFBQUFBTUp1SGhFUkFBQUE0MjVaUG1hUEFRREN3dm9VQ2dBQUFPUFdSdkxVa0FBQVlJek1IZnpwWWJRN2Q1d1pGUVdtNHRPL1JkV2syMFlZclhiSUxXRjFSVFZmQUFBQUFBQUFBRFZLQWdBQUFBQUF3NnJrY2xFUzhJQXdNSkpBNjNGTWtXcFQzQ1NvUjhZcUZaaks4WjNrN0dNZUFBQUFBQUFBQUIrNUFBQUFBQUFBQVFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBd0FBQUdKMWVRQT0iLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgaW52b2tlIFsyXSIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBjb25zdW1lZCAyMDU0IG9mIDM4Nzk2IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBjb25zdW1lZCA2NzE3OCBvZiAxMDI0ODYgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIl0="}'
2026-01-23T02:11:02.149081+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.190134+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.190147+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.190164+00:00 abstractendeavors env[2992447]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"56LvGqZj6JrHNEdNGLKZStjrZjCQpKDSW5iLS9wx2yvnPma6FYPdKSN37tMBGwF1i2LxfrfBDFYmq14U3FW64dVw","slot":395310303,"logs_b64":"WyJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGludm9rZSBbMV0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEV4dGVuZEFjY291bnQiLCJQcm9ncmFtIGxvZzogQWNjb3VudCBhbHJlYWR5IGhhcyB0aGUgY29ycmVjdCBzaXplIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDM2ODcgb2YgNDAyODUwIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzFdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBCdXkiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogaW52b2tlIFsyXSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogR2V0RmVlcyIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBjb25zdW1lZCAzMTIxIG9mIDM1MDQ2MiBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSByZXR1cm46IHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogQUFBQUFBQUFBQUJmQUFBQUFBQUFBQjRBQUFBQUFBQUEiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogc3VjY2VzcyIsIlByb2dyYW0gVG9rZW5rZWdRZmVaeWlOd0FKYk5iR0tQRlhDV3VCdmY5U3M2MjNWUTVEQSBpbnZva2UgWzJdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBUcmFuc2ZlckNoZWNrZWQiLCJQcm9ncmFtIFRva2Vua2VnUWZlWnlpTndBSmJOYkdLUEZYQ1d1QnZmOVNzNjIzVlE1REEgY29uc3VtZWQgNjE0NyBvZiAzNDM1MzMgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gVG9rZW5rZWdRZmVaeWlOd0FKYk5iR0tQRlhDV3VCdmY5U3M2MjNWUTVEQSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzJdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzJdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzJdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBkYXRhOiB2ZHQvMDA3bVllNXJUUHR6Skl5cVN2dU5LcWl0RWgwVVBmVExQbWEvZ3UrQ1d1MFZNY3pMVHllam1BQUFBQUFBeDA1WWh5Y0FBQUFCNlBDd2hpRHNBOXlRSE1iVFViOWpMQ21TZWlzaUNCa0dhSzkyTEZiQXlHKzEySEpwQUFBQUFLV0JIaVFLQUFBQW5zTmNpQ3FnQWdDbDFmb25Bd0FBQUo0clNqeVpvUUVBU3NMNDBOMWN2SmZqS0p3WmZMVUdLbFR6MlZhNXptNVJGZmxsWjZwY3MrWmZBQUFBQUFBQUFEZHpBUUFBQUFBQWJ4WmRqZTk3RkRyRitpN3NWbEt5NTVjVE1kaXZYbG43S1hTRS94TDFpMzhlQUFBQUFBQUFBRHAxQUFBQUFBQUFBUUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUF3QUFBR0oxZVFBPSIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzJdIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDIwNTQgb2YgMzI0NzIwIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBjb25zdW1lZCA3NzkzMSBvZiAzOTkxNjMgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIl0="}'
2026-01-23T02:11:02.190171+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.190413+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.190418+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.190430+00:00 abstractendeavors env[2992446]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"5TnMEfGktMYpGYax3pvEFZFaTcsFWkAGFvmJDHwEE5ER31Zt58ukxtJ4A8owSfTRczNRS6RMKyRNVrqgKyZJ7kTL","slot":395310303,"logs_b64":"WyJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBDb21wdXRlQnVkZ2V0MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzFdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBTZWxsIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEdldEZlZXMiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogY29uc3VtZWQgMzEyMSBvZiA1MDcyOSBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSByZXR1cm46IHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogQUFBQUFBQUFBQUJmQUFBQUFBQUFBQjRBQUFBQUFBQUEiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogc3VjY2VzcyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBpbnZva2UgWzJdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBUcmFuc2ZlckNoZWNrZWQiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgY29uc3VtZWQgMjM1NSBvZiA0Mzg0NCBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIHN1Y2Nlc3MiLCJQcm9ncmFtIGRhdGE6IHZkdC8wMDdtWWU0VFcxeDNsdWZBMkZIR0xNUi80Qzl4ekV2aUdNQ0NMY1oweWpsczVyTGtuNmI2bVJFQUFBQUFiQkIyY2hzRUFBQUEyekpNejJJTitFdTR0UUhKOGU2c3B1RUYwaDUyZlpPZFFyZ1hqT2FBSWRDMTJISnBBQUFBQU5DZzNLVUtBQUFBaXhiWlR5eUFBZ0RROUxpcEF3QUFBSXQreGdPYmdRRUFyUkhtcFB3cFJLVDZnbEcrK0JWQ2JodjdLTWEyWkdaM1lIeHEyZlZtcGtaZkFBQUFBQUFBQUl2T0tnQUFBQUFBRGdsNGlhSU1IMThsaU1CeVEyZFpnL1krc3UvYVh2QkpqbXhxMDNYSTBLY2VBQUFBQUFBQUFKaUVEUUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQkFBQUFITmxiR3dBIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGludm9rZSBbMl0iLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgY29uc3VtZWQgMjA1NCBvZiAzNDg4MiBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIHN1Y2Nlc3MiLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgY29uc3VtZWQgNDc2Mzcgb2YgNzk1NTAgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMV0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IENsb3NlQWNjb3VudCIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCAxMTU0IG9mIDMxOTEzIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyJd"}'
2026-01-23T02:11:02.190434+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.231469+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.231482+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.231500+00:00 abstractendeavors env[2992459]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"4zDfayJB66hMUkYbN64nChTmeydx1dH6damqz6FKYNRST4h7BGhvzvfvw8mouHFHpsW6xWjQJjsHxVs6vnAicfKt","slot":395310303,"logs_b64":"WyJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBDb21wdXRlQnVkZ2V0MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzFdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBTZWxsIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEdldEZlZXMiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogY29uc3VtZWQgMzEyMSBvZiA1MDcyOSBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSByZXR1cm46IHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogQUFBQUFBQUFBQUJmQUFBQUFBQUFBQjRBQUFBQUFBQUEiLCJQcm9ncmFtIHBmZWVVeEI2amtlWTFIeGQ3Q3NGQ0FqY2JIQTlyV3RjaE1HZFo2Vm9qVlogc3VjY2VzcyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBpbnZva2UgWzJdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBUcmFuc2ZlckNoZWNrZWQiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgY29uc3VtZWQgMjM1NSBvZiA0Mzg0NCBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIHN1Y2Nlc3MiLCJQcm9ncmFtIGRhdGE6IHZkdC8wMDdtWWU0VFcxeDNsdWZBMkZIR0xNUi80Qzl4ekV2aUdNQ0NMY1oweWpsczVyTGtud0NuNkJJQUFBQUFyTkMweG5nRUFBQUF2WVhFelJ2RldTbk1UQjBuMmxBUDczZWdhTlBLQUxqaUYyTEViWmZEdjR1MTJISnBBQUFBQU5ENTg1SUtBQUFBTitlTkZxV0VBZ0RRVGRDV0F3QUFBRGRQZThvVGhnRUFyUkhtcFB3cFJLVDZnbEcrK0JWQ2JodjdLTWEyWkdaM1lIeHEyZlZtcGtaZkFBQUFBQUFBQUhqOExRQUFBQUFBRGdsNGlhSU1IMThsaU1CeVEyZFpnL1krc3UvYVh2QkpqbXhxMDNYSTBLY2VBQUFBQUFBQUFKK0ZEZ0FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQkFBQUFITmxiR3dBIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGludm9rZSBbMl0iLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgY29uc3VtZWQgMjA1NCBvZiAzNDg4MiBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIHN1Y2Nlc3MiLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgY29uc3VtZWQgNDc2Mzcgb2YgNzk1NTAgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMV0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IENsb3NlQWNjb3VudCIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCAxMTU0IG9mIDMxOTEzIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyJd"}'
2026-01-23T02:11:02.231507+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.231823+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.231833+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.231863+00:00 abstractendeavors env[2992458]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"2NpJE215LPogUr66rbhmfUH1z7iNkdNMYQgLb3i8iVf7vPCiLk7TatF9oYjjSiratiQZjiqTf8SiB35xr8N7wpFF","slot":395310303,"logs_b64":"WyJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBDb21wdXRlQnVkZ2V0MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gQVRva2VuR1B2YmRHVnhyMWIyaHZaYnNpcVc1eFdIMjVlZlROc0xKQThrbkwgaW52b2tlIFsxXSIsIlByb2dyYW0gbG9nOiBDcmVhdGVJZGVtcG90ZW50IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEdldEFjY291bnREYXRhU2l6ZSIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCAxNDQ0IG9mIDE0NDIzMiBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSByZXR1cm46IFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgcWdBQUFBQUFBQUE9IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIHN1Y2Nlc3MiLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMl0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiLCJQcm9ncmFtIGxvZzogSW5pdGlhbGl6ZSB0aGUgYXNzb2NpYXRlZCB0b2tlbiBhY2NvdW50IiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbMl0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEluaXRpYWxpemVJbW11dGFibGVPd25lciIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCA2NzQgb2YgMTM3ODU4IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgc3VjY2VzcyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBpbnZva2UgWzJdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBJbml0aWFsaXplQWNjb3VudDMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgY29uc3VtZWQgMjAyNyBvZiAxMzQ3OTYgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBzdWNjZXNzIiwiUHJvZ3JhbSBBVG9rZW5HUHZiZEdWeHIxYjJodlpic2lxVzV4V0gyNWVmVE5zTEpBOGtuTCBjb25zdW1lZCAxNzA2NCBvZiAxNDk1NTAgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gQVRva2VuR1B2YmRHVnhyMWIyaHZaYnNpcVc1eFdIMjVlZlROc0xKQThrbkwgc3VjY2VzcyIsIlByb2dyYW0gRkxBU0hYOERyTGJnZVI4RmNmTlYxRjVrcnhZY1lNVWRCa3JQMUVQQnR4QjkgaW52b2tlIFsxXSIsIlByb2dyYW0gRjV0ZnZiTG9nOVZkR1VQcUJEVFQ4cmdYdlRUY3E3ZTVVaUdudXBMMXp2QnEgaW52b2tlIFsyXSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBpbnZva2UgWzNdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBHZXRGZWVzIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIGNvbnN1bWVkIDMxMjEgb2YgMTI2Njg0IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIHJldHVybjogcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBBQUFBQUFBQUFBQmZBQUFBQUFBQUFCNEFBQUFBQUFBQSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBzdWNjZXNzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGludm9rZSBbM10iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEJ1eSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBpbnZva2UgWzRdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBHZXRGZWVzIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIGNvbnN1bWVkIDMxMjEgb2YgODE0OTQgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gcmV0dXJuOiBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIEFBQUFBQUFBQUFCZkFBQUFBQUFBQUI0QUFBQUFBQUFBIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIHN1Y2Nlc3MiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgaW52b2tlIFs0XSIsIlByb2dyYW0gbG9nOiBJbnN0cnVjdGlvbjogVHJhbnNmZXJDaGVja2VkIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGNvbnN1bWVkIDI0NzUgb2YgNzQ1NzAgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzRdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzRdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzRdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBkYXRhOiB2ZHQvMDA3bVllNFRXMXgzbHVmQTJGSEdMTVIvNEM5eHpFdmlHTUNDTGNaMHlqbHM1ckxrbnpqODZRSUFBQUFBV1VJQWRyRUFBQUFCQmZuNk1XWXE0SWJ1cVh2LzdLN0ZCWTZsanNnZ1BMNCtYUHRJZURwZFNmNjEySEpwQUFBQUFBajIzWlVLQUFBQTNxU05vUE9EQWdBSVNycVpBd0FBQU40TWUxUmloUUVBNEFUSWZPdVkrbHprZjRBNEJ2MHNlVVhTbFNTVm11d0EzdGw0RlBPUGVFWmZBQUFBQUFBQUFEMFdCd0FBQUFBQURnbDRpYUlNSDE4bGlNQnlRMmRaZy9ZK3N1L2FYdkJKam14cTAzWEkwS2NlQUFBQUFBQUFBT3M4QWdBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUF3QUFBR0oxZVFBPSIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBpbnZva2UgWzRdIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDIwNTQgb2YgNTk0MjkgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGNvbnN1bWVkIDY0MTgxIG9mIDEyMDEyMiBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIHN1Y2Nlc3MiLCJQcm9ncmFtIEY1dGZ2YkxvZzlWZEdVUHFCRFRUOHJnWHZUVGNxN2U1VWlHbnVwTDF6dkJxIGNvbnN1bWVkIDcyNzk1IG9mIDEyODYyMSBjb21wdXRlIHVuaXRzIiwiUHJvZ3JhbSBGNXRmdmJMb2c5VmRHVVBxQkRUVDhyZ1h2VFRjcTdlNVVpR251cEwxenZCcSBzdWNjZXNzIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBpbnZva2UgWzJdIiwiUHJvZ3JhbSAxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBGTEFTSFg4RHJMYmdlUjhGY2ZOVjFGNWtyeFljWU1VZEJrclAxRVBCdHhCOSBjb25zdW1lZCA3ODU1OSBvZiAxMzI0ODYgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gRkxBU0hYOERyTGJnZVI4RmNmTlYxRjVrcnhZY1lNVWRCa3JQMUVQQnR4Qjkgc3VjY2VzcyJd"}'
2026-01-23T02:11:02.231871+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.272762+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.272770+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.272790+00:00 abstractendeavors env[2992447]:   message: 'logIntake recieved  {"program_id":"6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P","signature":"4WWAoLohpKNaJf33gGso3GJ45pfc1XXkvHdpxMA6Uy9MHCKoAx8KF7mVYRzvPWoXLvZ2gJWjFqDHzNm7euxQr4ah","slot":395310303,"logs_b64":"WyJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsxXSIsIlByb2dyYW0gQ29tcHV0ZUJ1ZGdldDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMSBzdWNjZXNzIiwiUHJvZ3JhbSBDb21wdXRlQnVkZ2V0MTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIENvbXB1dGVCdWRnZXQxMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gRkxBU0hYOERyTGJnZVI4RmNmTlYxRjVrcnhZY1lNVWRCa3JQMUVQQnR4QjkgaW52b2tlIFsxXSIsIlByb2dyYW0gRjV0ZnZiTG9nOVZkR1VQcUJEVFQ4cmdYdlRUY3E3ZTVVaUdudXBMMXp2QnEgaW52b2tlIFsyXSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBpbnZva2UgWzNdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBHZXRGZWVzIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIGNvbnN1bWVkIDMxMjEgb2YgMTQzOTAxIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIHJldHVybjogcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBBQUFBQUFBQUFBQmZBQUFBQUFBQUFCNEFBQUFBQUFBQSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBzdWNjZXNzIiwiUHJvZ3JhbSA2RUY4cnJlY3RoUjVEa3pvbjhOd3U3OGhSdmZDS3ViSjE0TTV1QkV3RjZQIGludm9rZSBbM10iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IEJ1eSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBpbnZva2UgWzRdIiwiUHJvZ3JhbSBsb2c6IEluc3RydWN0aW9uOiBHZXRGZWVzIiwiUHJvZ3JhbSBwZmVlVXhCNmprZVkxSHhkN0NzRkNBamNiSEE5cld0Y2hNR2RaNlZvalZaIGNvbnN1bWVkIDMxMjEgb2YgMTAwMjQxIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIHJldHVybjogcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBBQUFBQUFBQUFBQmZBQUFBQUFBQUFCNEFBQUFBQUFBQSIsIlByb2dyYW0gcGZlZVV4QjZqa2VZMUh4ZDdDc0ZDQWpjYkhBOXJXdGNoTUdkWjZWb2pWWiBzdWNjZXNzIiwiUHJvZ3JhbSBUb2tlbnpRZEJOYkxxUDVWRWhka0FTNkVQRkxDMVBIbkJxQ1hFcFB4dUViIGludm9rZSBbNF0iLCJQcm9ncmFtIGxvZzogSW5zdHJ1Y3Rpb246IFRyYW5zZmVyQ2hlY2tlZCIsIlByb2dyYW0gVG9rZW56UWRCTmJMcVA1VkVoZGtBUzZFUEZMQzFQSG5CcUNYRXBQeHVFYiBjb25zdW1lZCAyNDc1IG9mIDkzMzE3IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIFRva2VuelFkQk5iTHFQNVZFaGRrQVM2RVBGTEMxUEhuQnFDWEVwUHh1RWIgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFs0XSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFs0XSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFs0XSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gZGF0YTogdmR0LzAwN21ZZTVlQzBZb0RRd0FGM0x6ZHpPYnVXT3JTVzRQTUpiazZwYWFXNGw3MlJ5THI4ZmhUeGNBQUFBQWpzemYyRHNEQUFBQjhVL3MybzVMMU1zSlM1bTBWUzNpL0tuNjYvM2ZSQXBhWjQ4SHlyNTNHU3kxMkhKcEFBQUFBSzEyZCtZTkFBQUF0NFdNNW1McUFRQ3R5bFBxQmdBQUFMZnRlWnJSNndBQVk0TnpBQTZpTExKazAwci9aS0JMWHZxL3UzVGR6UVNKbDdHWUZVZlgwUkJmQUFBQUFBQUFBT1N4T0FBQUFBQUFMbU5HeFVpaHI5SEQzZ3NrRGFlZFlXZ3ZpMVE0WTNvSlVNdzZ5OE4xOTJRZUFBQUFBQUFBQUZibkVRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBd0FBQUdKMWVRQT0iLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgaW52b2tlIFs0XSIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBjb25zdW1lZCAyMDU0IG9mIDc4MTc2IGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIDZFRjhycmVjdGhSNURrem9uOE53dTc4aFJ2ZkNLdWJKMTRNNXVCRXdGNlAgc3VjY2VzcyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBjb25zdW1lZCA2MjY1MiBvZiAxMzczNDAgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gNkVGOHJyZWN0aFI1RGt6b244Tnd1NzhoUnZmQ0t1YkoxNE01dUJFd0Y2UCBzdWNjZXNzIiwiUHJvZ3JhbSBGNXRmdmJMb2c5VmRHVVBxQkRUVDhyZ1h2VFRjcTdlNVVpR251cEwxenZCcSBjb25zdW1lZCA3MTI2MyBvZiAxNDU4MzYgY29tcHV0ZSB1bml0cyIsIlByb2dyYW0gRjV0ZnZiTG9nOVZkR1VQcUJEVFQ4cmdYdlRUY3E3ZTVVaUdudXBMMXp2QnEgc3VjY2VzcyIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgaW52b2tlIFsyXSIsIlByb2dyYW0gMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTEgc3VjY2VzcyIsIlByb2dyYW0gRkxBU0hYOERyTGJnZVI4RmNmTlYxRjVrcnhZY1lNVWRCa3JQMUVQQnR4QjkgY29uc3VtZWQgNzcwMjEgb2YgMTQ5NzAwIGNvbXB1dGUgdW5pdHMiLCJQcm9ncmFtIEZMQVNIWDhEckxiZ2VSOEZjZk5WMUY1a3J4WWNZTVVkQmtyUDFFUEJ0eEI5IHN1Y2Nlc3MiLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIGludm9rZSBbMV0iLCJQcm9ncmFtIDExMTExMTExMTExMTExMTExMTExMTExMTExMTExMTExIHN1Y2Nlc3MiXQ=="}'
2026-01-23T02:11:02.272796+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.292563+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logIntake processed  3242724' }
2026-01-23T02:11:02.292593+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logIntake processed  3242726' }
2026-01-23T02:11:02.292600+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.292606+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.292611+00:00 abstractendeavors env[2992459]:   message: 'logIntake Sent  3242726 to logEntryQueue'
2026-01-23T02:11:02.292617+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.292623+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.292629+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.292634+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.292640+00:00 abstractendeavors env[2992459]:   details: { queue: 'logIntake', result: 3242726 }
2026-01-23T02:11:02.292646+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.292659+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.292665+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.292671+00:00 abstractendeavors env[2992447]:   message: 'logIntake Sent  3242724 to logEntryQueue'
2026-01-23T02:11:02.292677+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.292688+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.292694+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.292701+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:02.292706+00:00 abstractendeavors env[2992447]:   details: { queue: 'logIntake', result: 3242724 }
2026-01-23T02:11:02.292713+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.292728+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logIntake processed  3242723' }
2026-01-23T02:11:02.292736+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.292742+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.292756+00:00 abstractendeavors env[2992458]:   message: 'logIntake Sent  3242723 to logEntryQueue'
2026-01-23T02:11:02.292761+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.292767+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.292784+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.292790+00:00 abstractendeavors env[2992458]:   message: 'Queue handler',
2026-01-23T02:11:02.292795+00:00 abstractendeavors env[2992458]:   details: { queue: 'logIntake', result: 3242723 }
2026-01-23T02:11:02.292800+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.292814+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logIntake processed  3242721' }
2026-01-23T02:11:02.292820+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.292826+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.292832+00:00 abstractendeavors env[2992446]:   message: 'logIntake Sent  3242721 to logEntryQueue'
2026-01-23T02:11:02.292838+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.292844+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.292849+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.292855+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:02.292861+00:00 abstractendeavors env[2992446]:   details: { queue: 'logIntake', result: 3242721 }
2026-01-23T02:11:02.292867+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.292881+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry processed  3242590' }
2026-01-23T02:11:02.292886+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.292890+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.292894+00:00 abstractendeavors env[2992459]:   message: 'logEntry Sent  3242590 to txnEntryQueue'
2026-01-23T02:11:02.292898+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.292902+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.292906+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.292910+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.292914+00:00 abstractendeavors env[2992459]:   details: { queue: 'logEntry', result: 3242590 }
2026-01-23T02:11:02.292918+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.292927+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logIntake processed  3242722' }
2026-01-23T02:11:02.292931+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.292935+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.292939+00:00 abstractendeavors env[2992446]:   message: 'logIntake Sent  3242722 to logEntryQueue'
2026-01-23T02:11:02.292943+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.292947+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.292952+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.292956+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:02.292960+00:00 abstractendeavors env[2992446]:   details: { queue: 'logIntake', result: 3242722 }
2026-01-23T02:11:02.292965+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.293097+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.293104+00:00 abstractendeavors env[2992446]:   function_name: 'processTxns',
2026-01-23T02:11:02.293108+00:00 abstractendeavors env[2992446]:   message: 'Transaction processing completed',
2026-01-23T02:11:02.293112+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.293116+00:00 abstractendeavors env[2992446]:     signature: '2eZTYCHDTReBFhzrcxFQT7eVVwYK1aAGEub4yKd8DiArtqU5JqTqF7rgsBtwjTSAuMLLiRn2Gdjk2weFcV8Zhy5b',
2026-01-23T02:11:02.293120+00:00 abstractendeavors env[2992446]:     txn_id: undefined,
2026-01-23T02:11:02.293124+00:00 abstractendeavors env[2992446]:     pair_id: 52166,
2026-01-23T02:11:02.293128+00:00 abstractendeavors env[2992446]:     meta_id: 216862,
2026-01-23T02:11:02.293132+00:00 abstractendeavors env[2992446]:     log_id: 3049170
2026-01-23T02:11:02.293138+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:02.293143+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.293147+00:00 abstractendeavors env[2992446]:   logType: 'success'
2026-01-23T02:11:02.293151+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.293183+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'txnEntry processed  [object Object]' }
2026-01-23T02:11:02.293188+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.293192+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.293195+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:02.293197+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.293200+00:00 abstractendeavors env[2992446]:     queue: 'txnEntry',
2026-01-23T02:11:02.293203+00:00 abstractendeavors env[2992446]:     result: {
2026-01-23T02:11:02.293206+00:00 abstractendeavors env[2992446]:       signature: '2eZTYCHDTReBFhzrcxFQT7eVVwYK1aAGEub4yKd8DiArtqU5JqTqF7rgsBtwjTSAuMLLiRn2Gdjk2weFcV8Zhy5b',
2026-01-23T02:11:02.293209+00:00 abstractendeavors env[2992446]:       meta_id: 216862,
2026-01-23T02:11:02.293212+00:00 abstractendeavors env[2992446]:       log_id: 3049170,
2026-01-23T02:11:02.293215+00:00 abstractendeavors env[2992446]:       pair_id: 52166,
2026-01-23T02:11:02.293218+00:00 abstractendeavors env[2992446]:       mint: 'DmZVKmL9qhunaCv9f33U67L5sge14ktYjtvbMG9UH4FA',
2026-01-23T02:11:02.293221+00:00 abstractendeavors env[2992446]:       signatures: null,
2026-01-23T02:11:02.293223+00:00 abstractendeavors env[2992446]:       slot: 395279068,
2026-01-23T02:11:02.293226+00:00 abstractendeavors env[2992446]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.293230+00:00 abstractendeavors env[2992446]:       logs: [Array],
2026-01-23T02:11:02.293233+00:00 abstractendeavors env[2992446]:       tcns: [],
2026-01-23T02:11:02.293237+00:00 abstractendeavors env[2992446]:       sol_amount: 244616656n,
2026-01-23T02:11:02.293240+00:00 abstractendeavors env[2992446]:       token_amount: 2972677604421n,
2026-01-23T02:11:02.293242+00:00 abstractendeavors env[2992446]:       is_buy: false,
2026-01-23T02:11:02.293246+00:00 abstractendeavors env[2992446]:       user: 'DAKvFJUiMTPv9vynQE8YPvjeYDG5doAKQjQ3nP99Haau',
2026-01-23T02:11:02.293250+00:00 abstractendeavors env[2992446]:       timestamp: 1769121750n,
2026-01-23T02:11:02.293253+00:00 abstractendeavors env[2992446]:       virtual_sol_reserves: 51344925004n,
2026-01-23T02:11:02.293256+00:00 abstractendeavors env[2992446]:       virtual_token_reserves: 626936354232647n,
2026-01-23T02:11:02.293262+00:00 abstractendeavors env[2992446]:       real_sol_reserves: 21344925004n,
2026-01-23T02:11:02.293266+00:00 abstractendeavors env[2992446]:       real_token_reserves: 347036354232647n,
2026-01-23T02:11:02.293271+00:00 abstractendeavors env[2992446]:       fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.293274+00:00 abstractendeavors env[2992446]:       fee_basis_points: 95n,
2026-01-23T02:11:02.293278+00:00 abstractendeavors env[2992446]:       fee: 2323859n,
2026-01-23T02:11:02.293282+00:00 abstractendeavors env[2992446]:       creator: 'bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa',
2026-01-23T02:11:02.293285+00:00 abstractendeavors env[2992446]:       creator_fee_basis_points: 30n,
2026-01-23T02:11:02.293289+00:00 abstractendeavors env[2992446]:       creator_fee: 733850n,
2026-01-23T02:11:02.293292+00:00 abstractendeavors env[2992446]:       track_volume: false,
2026-01-23T02:11:02.293296+00:00 abstractendeavors env[2992446]:       total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.293303+00:00 abstractendeavors env[2992446]:       total_claimed_tokens: 0n,
2026-01-23T02:11:02.293307+00:00 abstractendeavors env[2992446]:       current_sol_volume: 0n,
2026-01-23T02:11:02.293314+00:00 abstractendeavors env[2992446]:       last_update_timestamp: 0n,
2026-01-23T02:11:02.293317+00:00 abstractendeavors env[2992446]:       ix_name: 'sell',
2026-01-23T02:11:02.293329+00:00 abstractendeavors env[2992446]:       mayhem_mode: false
2026-01-23T02:11:02.293336+00:00 abstractendeavors env[2992446]:     }
2026-01-23T02:11:02.293340+00:00 abstractendeavors env[2992446]:   }
2026-01-23T02:11:02.293343+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.293352+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.293356+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:02.293360+00:00 abstractendeavors env[2992447]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.293363+00:00 abstractendeavors env[2992447]:   details: {
2026-01-23T02:11:02.293367+00:00 abstractendeavors env[2992447]:     signature: '2K9dK1gnG6dbGNMXbphkbc2JadtTifMQUKwx7ZC76SY7Q4jiphSvc8eD3o8YFHGK8NsihjSfdmrP1LkYP9U4AuUV',
2026-01-23T02:11:02.293371+00:00 abstractendeavors env[2992447]:     slot: 395279121
2026-01-23T02:11:02.293376+00:00 abstractendeavors env[2992447]:   },
2026-01-23T02:11:02.293380+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.293384+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.293387+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.293396+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logIntake processed  3242720' }
2026-01-23T02:11:02.293399+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.293403+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.293408+00:00 abstractendeavors env[2992447]:   message: 'logIntake Sent  3242720 to logEntryQueue'
2026-01-23T02:11:02.293412+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.293419+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.293423+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.293427+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:02.293431+00:00 abstractendeavors env[2992447]:   details: { queue: 'logIntake', result: 3242720 }
2026-01-23T02:11:02.293435+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.293442+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.293446+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.293450+00:00 abstractendeavors env[2992459]:   message: 'Error processing transaction log',
2026-01-23T02:11:02.293454+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.293458+00:00 abstractendeavors env[2992459]:     error: '"null value in column \\"user_address\\" of relation \\"transactions\\" violates not-null constraint"',
2026-01-23T02:11:02.293462+00:00 abstractendeavors env[2992459]:     invocation: {
2026-01-23T02:11:02.293465+00:00 abstractendeavors env[2992459]:       data: [Array],
2026-01-23T02:11:02.293469+00:00 abstractendeavors env[2992459]:       logs: [Array],
2026-01-23T02:11:02.293473+00:00 abstractendeavors env[2992459]:       depth: 2,
2026-01-23T02:11:02.293476+00:00 abstractendeavors env[2992459]:       compute: [Object],
2026-01-23T02:11:02.293480+00:00 abstractendeavors env[2992459]:       children: [Array],
2026-01-23T02:11:02.293483+00:00 abstractendeavors env[2992459]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.293487+00:00 abstractendeavors env[2992459]:       invocation_index: 10,
2026-01-23T02:11:02.293491+00:00 abstractendeavors env[2992459]:       reported_invocation: 3
2026-01-23T02:11:02.293495+00:00 abstractendeavors env[2992459]:     }
2026-01-23T02:11:02.293498+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.293502+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.293505+00:00 abstractendeavors env[2992459]:   logType: 'error'
2026-01-23T02:11:02.293509+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.293596+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.293603+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.293607+00:00 abstractendeavors env[2992458]:   message: 'metaDataCall processed  [object Object]'
2026-01-23T02:11:02.293611+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.293647+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.293653+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.293655+00:00 abstractendeavors env[2992458]:   message: 'Queue handler',
2026-01-23T02:11:02.293659+00:00 abstractendeavors env[2992458]:   details: {
2026-01-23T02:11:02.293666+00:00 abstractendeavors env[2992458]:     queue: 'metaDataCall',
2026-01-23T02:11:02.293669+00:00 abstractendeavors env[2992458]:     result: MetaDataRow {
2026-01-23T02:11:02.293674+00:00 abstractendeavors env[2992458]:       id: 54399,
2026-01-23T02:11:02.293678+00:00 abstractendeavors env[2992458]:       mint: '8K7EBnqSnFxHahxxeWrQw4awU7ZuBd6w9HbbQYgdpump',
2026-01-23T02:11:02.293682+00:00 abstractendeavors env[2992458]:       metadata_pda: null,
2026-01-23T02:11:02.293686+00:00 abstractendeavors env[2992458]:       update_authority: null,
2026-01-23T02:11:02.293690+00:00 abstractendeavors env[2992458]:       discriminator: null,
2026-01-23T02:11:02.293694+00:00 abstractendeavors env[2992458]:       name: null,
2026-01-23T02:11:02.293698+00:00 abstractendeavors env[2992458]:       symbol: null,
2026-01-23T02:11:02.293701+00:00 abstractendeavors env[2992458]:       uri: null,
2026-01-23T02:11:02.293704+00:00 abstractendeavors env[2992458]:       user_address: null,
2026-01-23T02:11:02.293707+00:00 abstractendeavors env[2992458]:       genesis_signature: null,
2026-01-23T02:11:02.293709+00:00 abstractendeavors env[2992458]:       bonding_curve: null,
2026-01-23T02:11:02.293716+00:00 abstractendeavors env[2992458]:       associated_bonding_curve: null,
2026-01-23T02:11:02.293719+00:00 abstractendeavors env[2992458]:       program_id: null,
2026-01-23T02:11:02.293722+00:00 abstractendeavors env[2992458]:       seller_fee_basis_points: null,
2026-01-23T02:11:02.293724+00:00 abstractendeavors env[2992458]:       is_mutable: null,
2026-01-23T02:11:02.293727+00:00 abstractendeavors env[2992458]:       primary_sale_happened: null,
2026-01-23T02:11:02.293733+00:00 abstractendeavors env[2992458]:       token_standard: null,
2026-01-23T02:11:02.293736+00:00 abstractendeavors env[2992458]:       image: null,
2026-01-23T02:11:02.293740+00:00 abstractendeavors env[2992458]:       description: null,
2026-01-23T02:11:02.293743+00:00 abstractendeavors env[2992458]:       external_url: null,
2026-01-23T02:11:02.293747+00:00 abstractendeavors env[2992458]:       onchain_metadata: null,
2026-01-23T02:11:02.293751+00:00 abstractendeavors env[2992458]:       offchain_metadata: [Array],
2026-01-23T02:11:02.293755+00:00 abstractendeavors env[2992458]:       has_metadata: true,
2026-01-23T02:11:02.293759+00:00 abstractendeavors env[2992458]:       meta_created_at: null,
2026-01-23T02:11:02.293762+00:00 abstractendeavors env[2992458]:       created_at: 2026-01-20T17:39:53.432Z,
2026-01-23T02:11:02.293766+00:00 abstractendeavors env[2992458]:       updated_at: 2026-01-20T17:39:54.284Z,
2026-01-23T02:11:02.293771+00:00 abstractendeavors env[2992458]:       processed_at: null
2026-01-23T02:11:02.293775+00:00 abstractendeavors env[2992458]:     }
2026-01-23T02:11:02.293779+00:00 abstractendeavors env[2992458]:   }
2026-01-23T02:11:02.293782+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.293793+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logEntry recieved  {"id":3242722}' }
2026-01-23T02:11:02.293797+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.293800+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:02.293804+00:00 abstractendeavors env[2992447]:   message: 'pairData_',
2026-01-23T02:11:02.293810+00:00 abstractendeavors env[2992447]:   details: null,
2026-01-23T02:11:02.293814+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.293818+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.293822+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.293825+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.293829+00:00 abstractendeavors env[2992447]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:02.293833+00:00 abstractendeavors env[2992447]:   message: 'processMetaData',
2026-01-23T02:11:02.293837+00:00 abstractendeavors env[2992447]:   details: '48aL3fo3k2YouVatANK9LjBxqdcF35R3Xx1BDVGTrV5TBFPG8DQNruHa2TsNJhVtpgNm35FARJV66hg8rmjD4DQp',
2026-01-23T02:11:02.293841+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.293845+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.293849+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.293858+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry recieved  {"id":3242726}' }
2026-01-23T02:11:02.293862+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry recieved  {"id":3242720}' }
2026-01-23T02:11:02.293870+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logIntake processed  3242725' }
2026-01-23T02:11:02.293877+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logEntry recieved  {"id":3242723}' }
2026-01-23T02:11:02.293911+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.293915+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.293919+00:00 abstractendeavors env[2992446]:   message: 'logIntake Sent  3242725 to logEntryQueue'
2026-01-23T02:11:02.293922+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.293926+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.293930+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.293933+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:02.293937+00:00 abstractendeavors env[2992446]:   details: { queue: 'logIntake', result: 3242725 }
2026-01-23T02:11:02.293940+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.293997+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.294002+00:00 abstractendeavors env[2992446]:   function_name: 'processTxns',
2026-01-23T02:11:02.294008+00:00 abstractendeavors env[2992446]:   message: 'Transaction processing completed',
2026-01-23T02:11:02.294011+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.294016+00:00 abstractendeavors env[2992446]:     signature: '3S5c5LzT2ubExSVUBva3P6DSmiUX62VYuRg3A6kRfepsE2jbNgFKEcf6UBi3f6jwuVt4QzVHFPcAJkvpTs3THTLp',
2026-01-23T02:11:02.294020+00:00 abstractendeavors env[2992446]:     txn_id: undefined,
2026-01-23T02:11:02.294025+00:00 abstractendeavors env[2992446]:     pair_id: 52361,
2026-01-23T02:11:02.294028+00:00 abstractendeavors env[2992446]:     meta_id: 217285,
2026-01-23T02:11:02.294032+00:00 abstractendeavors env[2992446]:     log_id: 3049005
2026-01-23T02:11:02.294035+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:02.294039+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.294042+00:00 abstractendeavors env[2992446]:   logType: 'success'
2026-01-23T02:11:02.294046+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.294050+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'txnEntry processed  [object Object]' }
2026-01-23T02:11:02.294058+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.294061+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.294065+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:02.294069+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.294073+00:00 abstractendeavors env[2992446]:     queue: 'txnEntry',
2026-01-23T02:11:02.294076+00:00 abstractendeavors env[2992446]:     result: {
2026-01-23T02:11:02.294081+00:00 abstractendeavors env[2992446]:       signature: '3S5c5LzT2ubExSVUBva3P6DSmiUX62VYuRg3A6kRfepsE2jbNgFKEcf6UBi3f6jwuVt4QzVHFPcAJkvpTs3THTLp',
2026-01-23T02:11:02.294084+00:00 abstractendeavors env[2992446]:       meta_id: 217285,
2026-01-23T02:11:02.294088+00:00 abstractendeavors env[2992446]:       log_id: 3049005,
2026-01-23T02:11:02.294091+00:00 abstractendeavors env[2992446]:       pair_id: 52361,
2026-01-23T02:11:02.294095+00:00 abstractendeavors env[2992446]:       mint: 'FgNuGY4us9F2hWWKan6vv1DFNEyEEvBHMcxcjUDXpump',
2026-01-23T02:11:02.294100+00:00 abstractendeavors env[2992446]:       signatures: null,
2026-01-23T02:11:02.294103+00:00 abstractendeavors env[2992446]:       slot: 395279049,
2026-01-23T02:11:02.294107+00:00 abstractendeavors env[2992446]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.294111+00:00 abstractendeavors env[2992446]:       logs: [Array],
2026-01-23T02:11:02.294115+00:00 abstractendeavors env[2992446]:       tcns: [],
2026-01-23T02:11:02.294123+00:00 abstractendeavors env[2992446]:       sol_amount: 24444444n,
2026-01-23T02:11:02.294127+00:00 abstractendeavors env[2992446]:       token_amount: 294315512419n,
2026-01-23T02:11:02.294130+00:00 abstractendeavors env[2992446]:       is_buy: true,
2026-01-23T02:11:02.294133+00:00 abstractendeavors env[2992446]:       user: '5udWC5KaNJdaw6z5qNSQLMVnUV2mr7xr8rThX3ikfE2L',
2026-01-23T02:11:02.294136+00:00 abstractendeavors env[2992446]:       timestamp: 1769121742n,
2026-01-23T02:11:02.294138+00:00 abstractendeavors env[2992446]:       virtual_sol_reserves: 51718587018n,
2026-01-23T02:11:02.294145+00:00 abstractendeavors env[2992446]:       virtual_token_reserves: 622406795620502n,
2026-01-23T02:11:02.294148+00:00 abstractendeavors env[2992446]:       real_sol_reserves: 21718587018n,
2026-01-23T02:11:02.294153+00:00 abstractendeavors env[2992446]:       real_token_reserves: 342506795620502n,
2026-01-23T02:11:02.294156+00:00 abstractendeavors env[2992446]:       fee_recipient: 'G5UZAVbAf46s7cKWoyKu8kYTip9DGTpbLZ2qa9Aq69dP',
2026-01-23T02:11:02.294159+00:00 abstractendeavors env[2992446]:       fee_basis_points: 95n,
2026-01-23T02:11:02.294162+00:00 abstractendeavors env[2992446]:       fee: 232223n,
2026-01-23T02:11:02.294165+00:00 abstractendeavors env[2992446]:       creator: '6HkWQYbHeTRXsu1SdRHWpaoMfhkvJT4F7sDE39LEtpJs',
2026-01-23T02:11:02.294168+00:00 abstractendeavors env[2992446]:       creator_fee_basis_points: 30n,
2026-01-23T02:11:02.294170+00:00 abstractendeavors env[2992446]:       creator_fee: 73334n,
2026-01-23T02:11:02.294173+00:00 abstractendeavors env[2992446]:       track_volume: false,
2026-01-23T02:11:02.294176+00:00 abstractendeavors env[2992446]:       total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.294180+00:00 abstractendeavors env[2992446]:       total_claimed_tokens: 0n,
2026-01-23T02:11:02.294183+00:00 abstractendeavors env[2992446]:       current_sol_volume: 0n,
2026-01-23T02:11:02.294187+00:00 abstractendeavors env[2992446]:       last_update_timestamp: 0n,
2026-01-23T02:11:02.294191+00:00 abstractendeavors env[2992446]:       ix_name: 'buy',
2026-01-23T02:11:02.294195+00:00 abstractendeavors env[2992446]:       mayhem_mode: false
2026-01-23T02:11:02.294199+00:00 abstractendeavors env[2992446]:     }
2026-01-23T02:11:02.294203+00:00 abstractendeavors env[2992446]:   }
2026-01-23T02:11:02.294207+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.294217+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry processed  3242508' }
2026-01-23T02:11:02.294221+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.294225+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.294229+00:00 abstractendeavors env[2992446]:   message: 'logEntry Sent  3242508 to txnEntryQueue'
2026-01-23T02:11:02.294233+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.294237+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.294241+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.294245+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:02.294249+00:00 abstractendeavors env[2992446]:   details: { queue: 'logEntry', result: 3242508 }
2026-01-23T02:11:02.294253+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.294262+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.294267+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.294270+00:00 abstractendeavors env[2992446]:   message: 'pairData_',
2026-01-23T02:11:02.294274+00:00 abstractendeavors env[2992446]:   details: null,
2026-01-23T02:11:02.294277+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.294280+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.294285+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.294288+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.294291+00:00 abstractendeavors env[2992446]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:02.294294+00:00 abstractendeavors env[2992446]:   message: 'processMetaData',
2026-01-23T02:11:02.294297+00:00 abstractendeavors env[2992446]:   details: '3UeBAXkDFT5NqB14cJ4PxBcyDYQR3xmDFcC11JjbcThTJNug4vAjeV1hpp7Z3YuGXXJm7q9An4VRmzCSrKncHsYf',
2026-01-23T02:11:02.294300+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.294303+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.294305+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.294311+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.294315+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:02.294323+00:00 abstractendeavors env[2992447]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.294327+00:00 abstractendeavors env[2992447]:   details: {
2026-01-23T02:11:02.294329+00:00 abstractendeavors env[2992447]:     signature: '5T6hr1Av4FEYXB2fLAck1nPPv67YmX76TovRAN6pGx6EHBRxxfuEnw3Naeu4UYmE6p6HuCfEE8B94wxvu8N1kwpj',
2026-01-23T02:11:02.294332+00:00 abstractendeavors env[2992447]:     slot: 395279086
2026-01-23T02:11:02.294335+00:00 abstractendeavors env[2992447]:   },
2026-01-23T02:11:02.294338+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.294341+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.294343+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.294385+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.294388+00:00 abstractendeavors env[2992447]:   mint: '1EnUHUi9nM6yRGZzLuY9DWR6XjYP9aYPZKbXxxvpwcw',
2026-01-23T02:11:02.294391+00:00 abstractendeavors env[2992447]:   sol_amount: 194311336n,
2026-01-23T02:11:02.294394+00:00 abstractendeavors env[2992447]:   token_amount: 6850659773700n,
2026-01-23T02:11:02.294399+00:00 abstractendeavors env[2992447]:   is_buy: false,
2026-01-23T02:11:02.294405+00:00 abstractendeavors env[2992447]:   user: '97YgjgjVjebbAX1eZgzPXRMv3CvJC8joc2G8yMy4qD9g',
2026-01-23T02:11:02.294410+00:00 abstractendeavors env[2992447]:   timestamp: 1769121758n,
2026-01-23T02:11:02.294415+00:00 abstractendeavors env[2992447]:   virtual_sol_reserves: 30119444882n,
2026-01-23T02:11:02.294420+00:00 abstractendeavors env[2992447]:   virtual_token_reserves: 1068744797023877n,
2026-01-23T02:11:02.294425+00:00 abstractendeavors env[2992447]:   real_sol_reserves: 119444882n,
2026-01-23T02:11:02.294429+00:00 abstractendeavors env[2992447]:   real_token_reserves: 788844797023877n,
2026-01-23T02:11:02.294434+00:00 abstractendeavors env[2992447]:   fee_recipient: 'G5UZAVbAf46s7cKWoyKu8kYTip9DGTpbLZ2qa9Aq69dP',
2026-01-23T02:11:02.294439+00:00 abstractendeavors env[2992447]:   fee_basis_points: 95n,
2026-01-23T02:11:02.294444+00:00 abstractendeavors env[2992447]:   fee: 1845958n,
2026-01-23T02:11:02.294449+00:00 abstractendeavors env[2992447]:   creator: '8Mw8NBU3NkA5N4EQT2gzyyqvciJ35477PhmBuRC2QR6T',
2026-01-23T02:11:02.294454+00:00 abstractendeavors env[2992447]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.294459+00:00 abstractendeavors env[2992447]:   creator_fee: 582935n,
2026-01-23T02:11:02.294462+00:00 abstractendeavors env[2992447]:   track_volume: false,
2026-01-23T02:11:02.294466+00:00 abstractendeavors env[2992447]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.294469+00:00 abstractendeavors env[2992447]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.294473+00:00 abstractendeavors env[2992447]:   current_sol_volume: 0n,
2026-01-23T02:11:02.294476+00:00 abstractendeavors env[2992447]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.294480+00:00 abstractendeavors env[2992447]:   ix_name: 'sell',
2026-01-23T02:11:02.294485+00:00 abstractendeavors env[2992447]:   mayhem_mode: false
2026-01-23T02:11:02.294490+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.294500+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.294504+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:02.294508+00:00 abstractendeavors env[2992447]:   message: 'decodedData',
2026-01-23T02:11:02.294511+00:00 abstractendeavors env[2992447]:   details: {
2026-01-23T02:11:02.294514+00:00 abstractendeavors env[2992447]:     mint: '1EnUHUi9nM6yRGZzLuY9DWR6XjYP9aYPZKbXxxvpwcw',
2026-01-23T02:11:02.294518+00:00 abstractendeavors env[2992447]:     sol_amount: 194311336n,
2026-01-23T02:11:02.294521+00:00 abstractendeavors env[2992447]:     token_amount: 6850659773700n,
2026-01-23T02:11:02.294525+00:00 abstractendeavors env[2992447]:     is_buy: false,
2026-01-23T02:11:02.294528+00:00 abstractendeavors env[2992447]:     user: '97YgjgjVjebbAX1eZgzPXRMv3CvJC8joc2G8yMy4qD9g',
2026-01-23T02:11:02.294531+00:00 abstractendeavors env[2992447]:     timestamp: 1769121758n,
2026-01-23T02:11:02.294535+00:00 abstractendeavors env[2992447]:     virtual_sol_reserves: 30119444882n,
2026-01-23T02:11:02.294538+00:00 abstractendeavors env[2992447]:     virtual_token_reserves: 1068744797023877n,
2026-01-23T02:11:02.294543+00:00 abstractendeavors env[2992447]:     real_sol_reserves: 119444882n,
2026-01-23T02:11:02.294548+00:00 abstractendeavors env[2992447]:     real_token_reserves: 788844797023877n,
2026-01-23T02:11:02.294552+00:00 abstractendeavors env[2992447]:     fee_recipient: 'G5UZAVbAf46s7cKWoyKu8kYTip9DGTpbLZ2qa9Aq69dP',
2026-01-23T02:11:02.294557+00:00 abstractendeavors env[2992447]:     fee_basis_points: 95n,
2026-01-23T02:11:02.294562+00:00 abstractendeavors env[2992447]:     fee: 1845958n,
2026-01-23T02:11:02.294566+00:00 abstractendeavors env[2992447]:     creator: '8Mw8NBU3NkA5N4EQT2gzyyqvciJ35477PhmBuRC2QR6T',
2026-01-23T02:11:02.294571+00:00 abstractendeavors env[2992447]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.294576+00:00 abstractendeavors env[2992447]:     creator_fee: 582935n,
2026-01-23T02:11:02.294580+00:00 abstractendeavors env[2992447]:     track_volume: false,
2026-01-23T02:11:02.294585+00:00 abstractendeavors env[2992447]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.294588+00:00 abstractendeavors env[2992447]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.294592+00:00 abstractendeavors env[2992447]:     current_sol_volume: 0n,
2026-01-23T02:11:02.294595+00:00 abstractendeavors env[2992447]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.294598+00:00 abstractendeavors env[2992447]:     ix_name: 'sell',
2026-01-23T02:11:02.294602+00:00 abstractendeavors env[2992447]:     mayhem_mode: false
2026-01-23T02:11:02.294605+00:00 abstractendeavors env[2992447]:   },
2026-01-23T02:11:02.294608+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.294614+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.294617+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.294625+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.294630+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:02.294635+00:00 abstractendeavors env[2992458]:   message: 'Error processing transaction log',
2026-01-23T02:11:02.294639+00:00 abstractendeavors env[2992458]:   details: {
2026-01-23T02:11:02.294644+00:00 abstractendeavors env[2992458]:     error: '"null value in column \\"user_address\\" of relation \\"transactions\\" violates not-null constraint"',
2026-01-23T02:11:02.294649+00:00 abstractendeavors env[2992458]:     invocation: {
2026-01-23T02:11:02.294655+00:00 abstractendeavors env[2992458]:       data: [Array],
2026-01-23T02:11:02.294660+00:00 abstractendeavors env[2992458]:       logs: [Array],
2026-01-23T02:11:02.294666+00:00 abstractendeavors env[2992458]:       depth: 0,
2026-01-23T02:11:02.294670+00:00 abstractendeavors env[2992458]:       compute: [Object],
2026-01-23T02:11:02.294673+00:00 abstractendeavors env[2992458]:       children: [Array],
2026-01-23T02:11:02.294677+00:00 abstractendeavors env[2992458]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.294681+00:00 abstractendeavors env[2992458]:       invocation_index: 3,
2026-01-23T02:11:02.294684+00:00 abstractendeavors env[2992458]:       reported_invocation: 1
2026-01-23T02:11:02.294689+00:00 abstractendeavors env[2992458]:     }
2026-01-23T02:11:02.294695+00:00 abstractendeavors env[2992458]:   },
2026-01-23T02:11:02.294700+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.294704+00:00 abstractendeavors env[2992458]:   logType: 'error'
2026-01-23T02:11:02.294708+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.294720+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry recieved  {"id":3242721}' }
2026-01-23T02:11:02.294725+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'txnEntry recieved  {"id":3049669}' }
2026-01-23T02:11:02.294729+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry recieved  {"id":3242724}' }
2026-01-23T02:11:02.294734+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.294739+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.294743+00:00 abstractendeavors env[2992446]:   message: 'pairData_',
2026-01-23T02:11:02.294748+00:00 abstractendeavors env[2992446]:   details: null,
2026-01-23T02:11:02.294753+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.294757+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.294762+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.294766+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.294771+00:00 abstractendeavors env[2992446]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:02.294776+00:00 abstractendeavors env[2992446]:   message: 'processMetaData',
2026-01-23T02:11:02.294781+00:00 abstractendeavors env[2992446]:   details: '4ufN9UsQXNVtB3oqunQ462V6cndW9jyTL4RDxFuLQw3geCbpzEg942Ugt6iBvDP5mjUVNKTcZHXAXFhYqtFnHEnp',
2026-01-23T02:11:02.294787+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.294791+00:00 abstractendeavors env[2992446]:   logType: 'processing'
2026-01-23T02:11:02.294797+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.294808+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.294813+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:02.294818+00:00 abstractendeavors env[2992447]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.294824+00:00 abstractendeavors env[2992447]:   details: {
2026-01-23T02:11:02.294829+00:00 abstractendeavors env[2992447]:     signature: '2YaMziFfeVDKJBfuJMMe3WVb4pUsGT7A3AfYb2MQLadoqaywHf5Y2ygjLQbjYm87cohQXhZQKMCT3uUmetsn2diq',
2026-01-23T02:11:02.294834+00:00 abstractendeavors env[2992447]:     slot: 395279092
2026-01-23T02:11:02.294838+00:00 abstractendeavors env[2992447]:   },
2026-01-23T02:11:02.294843+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.294848+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.294852+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.294856+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.294861+00:00 abstractendeavors env[2992447]:   mint: 'E6MAyPJe3hqLHfK5mha5vwbi2TKFGUbriyn4tEe1pump',
2026-01-23T02:11:02.294866+00:00 abstractendeavors env[2992447]:   sol_amount: 491358023n,
2026-01-23T02:11:02.294872+00:00 abstractendeavors env[2992447]:   token_amount: 5211224337067n,
2026-01-23T02:11:02.294877+00:00 abstractendeavors env[2992447]:   is_buy: true,
2026-01-23T02:11:02.294883+00:00 abstractendeavors env[2992447]:   user: '8NXYWZFSNZfx7V7kSd11yqkZkWfh5xY4pafYEWK45nW',
2026-01-23T02:11:02.294887+00:00 abstractendeavors env[2992447]:   timestamp: 1769121760n,
2026-01-23T02:11:02.294892+00:00 abstractendeavors env[2992447]:   virtual_sol_reserves: 55338365257n,
2026-01-23T02:11:02.294897+00:00 abstractendeavors env[2992447]:   virtual_token_reserves: 581694091750207n,
2026-01-23T02:11:02.294902+00:00 abstractendeavors env[2992447]:   real_sol_reserves: 25338365257n,
2026-01-23T02:11:02.294907+00:00 abstractendeavors env[2992447]:   real_token_reserves: 301794091750207n,
2026-01-23T02:11:02.294911+00:00 abstractendeavors env[2992447]:   fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.294916+00:00 abstractendeavors env[2992447]:   fee_basis_points: 95n,
2026-01-23T02:11:02.294920+00:00 abstractendeavors env[2992447]:   fee: 4667902n,
2026-01-23T02:11:02.294925+00:00 abstractendeavors env[2992447]:   creator: 'FqTskkpwbtXGUxjPHtMu2wdTvTCWiSATcFHQ8vWG3msG',
2026-01-23T02:11:02.294930+00:00 abstractendeavors env[2992447]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.294934+00:00 abstractendeavors env[2992447]:   creator_fee: 1474075n,
2026-01-23T02:11:02.294939+00:00 abstractendeavors env[2992447]:   track_volume: false,
2026-01-23T02:11:02.294943+00:00 abstractendeavors env[2992447]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.294948+00:00 abstractendeavors env[2992447]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.294952+00:00 abstractendeavors env[2992447]:   current_sol_volume: 0n,
2026-01-23T02:11:02.294957+00:00 abstractendeavors env[2992447]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.294962+00:00 abstractendeavors env[2992447]:   ix_name: 'buy',
2026-01-23T02:11:02.294968+00:00 abstractendeavors env[2992447]:   mayhem_mode: false
2026-01-23T02:11:02.294972+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.294978+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.294983+00:00 abstractendeavors env[2992447]:   function_name: 'getTcns',
2026-01-23T02:11:02.294987+00:00 abstractendeavors env[2992447]:   message: 'decodedData',
2026-01-23T02:11:02.294992+00:00 abstractendeavors env[2992447]:   details: {
2026-01-23T02:11:02.294998+00:00 abstractendeavors env[2992447]:     mint: 'E6MAyPJe3hqLHfK5mha5vwbi2TKFGUbriyn4tEe1pump',
2026-01-23T02:11:02.295003+00:00 abstractendeavors env[2992447]:     sol_amount: 491358023n,
2026-01-23T02:11:02.295007+00:00 abstractendeavors env[2992447]:     token_amount: 5211224337067n,
2026-01-23T02:11:02.295012+00:00 abstractendeavors env[2992447]:     is_buy: true,
2026-01-23T02:11:02.295017+00:00 abstractendeavors env[2992447]:     user: '8NXYWZFSNZfx7V7kSd11yqkZkWfh5xY4pafYEWK45nW',
2026-01-23T02:11:02.295022+00:00 abstractendeavors env[2992447]:     timestamp: 1769121760n,
2026-01-23T02:11:02.295026+00:00 abstractendeavors env[2992447]:     virtual_sol_reserves: 55338365257n,
2026-01-23T02:11:02.295032+00:00 abstractendeavors env[2992447]:     virtual_token_reserves: 581694091750207n,
2026-01-23T02:11:02.295037+00:00 abstractendeavors env[2992447]:     real_sol_reserves: 25338365257n,
2026-01-23T02:11:02.295042+00:00 abstractendeavors env[2992447]:     real_token_reserves: 301794091750207n,
2026-01-23T02:11:02.295047+00:00 abstractendeavors env[2992447]:     fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.295053+00:00 abstractendeavors env[2992447]:     fee_basis_points: 95n,
2026-01-23T02:11:02.295057+00:00 abstractendeavors env[2992447]:     fee: 4667902n,
2026-01-23T02:11:02.295063+00:00 abstractendeavors env[2992447]:     creator: 'FqTskkpwbtXGUxjPHtMu2wdTvTCWiSATcFHQ8vWG3msG',
2026-01-23T02:11:02.295067+00:00 abstractendeavors env[2992447]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.295073+00:00 abstractendeavors env[2992447]:     creator_fee: 1474075n,
2026-01-23T02:11:02.295077+00:00 abstractendeavors env[2992447]:     track_volume: false,
2026-01-23T02:11:02.295082+00:00 abstractendeavors env[2992447]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.295086+00:00 abstractendeavors env[2992447]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.295091+00:00 abstractendeavors env[2992447]:     current_sol_volume: 0n,
2026-01-23T02:11:02.295095+00:00 abstractendeavors env[2992447]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.295100+00:00 abstractendeavors env[2992447]:     ix_name: 'buy',
2026-01-23T02:11:02.295104+00:00 abstractendeavors env[2992447]:     mayhem_mode: false
2026-01-23T02:11:02.295109+00:00 abstractendeavors env[2992447]:   },
2026-01-23T02:11:02.295114+00:00 abstractendeavors env[2992447]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.295118+00:00 abstractendeavors env[2992447]:   logType: 'processing'
2026-01-23T02:11:02.295123+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.295128+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logEntry recieved  {"id":3242725}' }
2026-01-23T02:11:02.295137+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.295142+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.295147+00:00 abstractendeavors env[2992446]:   message: 'Error processing transaction log',
2026-01-23T02:11:02.295153+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.295158+00:00 abstractendeavors env[2992446]:     error: '"null value in column \\"user_address\\" of relation \\"transactions\\" violates not-null constraint"',
2026-01-23T02:11:02.295163+00:00 abstractendeavors env[2992446]:     invocation: {
2026-01-23T02:11:02.295168+00:00 abstractendeavors env[2992446]:       data: [Array],
2026-01-23T02:11:02.295173+00:00 abstractendeavors env[2992446]:       logs: [Array],
2026-01-23T02:11:02.295177+00:00 abstractendeavors env[2992446]:       depth: 2,
2026-01-23T02:11:02.295183+00:00 abstractendeavors env[2992446]:       compute: [Object],
2026-01-23T02:11:02.295188+00:00 abstractendeavors env[2992446]:       children: [Array],
2026-01-23T02:11:02.295193+00:00 abstractendeavors env[2992446]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.295198+00:00 abstractendeavors env[2992446]:       invocation_index: 5,
2026-01-23T02:11:02.295204+00:00 abstractendeavors env[2992446]:       reported_invocation: 3
2026-01-23T02:11:02.295209+00:00 abstractendeavors env[2992446]:     }
2026-01-23T02:11:02.295213+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:02.295218+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.295223+00:00 abstractendeavors env[2992446]:   logType: 'error'
2026-01-23T02:11:02.295229+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.295240+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.295246+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.295251+00:00 abstractendeavors env[2992447]:   message: 'metaDataCall processed  [object Object]'
2026-01-23T02:11:02.295256+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.295260+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.295266+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.295270+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:02.295275+00:00 abstractendeavors env[2992447]:   details: {
2026-01-23T02:11:02.295280+00:00 abstractendeavors env[2992447]:     queue: 'metaDataCall',
2026-01-23T02:11:02.295287+00:00 abstractendeavors env[2992447]:     result: MetaDataRow {
2026-01-23T02:11:02.295291+00:00 abstractendeavors env[2992447]:       id: 54726,
2026-01-23T02:11:02.295295+00:00 abstractendeavors env[2992447]:       mint: '9VgYQ9cEr967xz7QmCtymRFFGrh1bkh81HEGFeZ5pump',
2026-01-23T02:11:02.295298+00:00 abstractendeavors env[2992447]:       metadata_pda: null,
2026-01-23T02:11:02.295302+00:00 abstractendeavors env[2992447]:       update_authority: null,
2026-01-23T02:11:02.295305+00:00 abstractendeavors env[2992447]:       discriminator: null,
2026-01-23T02:11:02.295309+00:00 abstractendeavors env[2992447]:       name: null,
2026-01-23T02:11:02.295312+00:00 abstractendeavors env[2992447]:       symbol: null,
2026-01-23T02:11:02.295317+00:00 abstractendeavors env[2992447]:       uri: null,
2026-01-23T02:11:02.295327+00:00 abstractendeavors env[2992447]:       user_address: null,
2026-01-23T02:11:02.295331+00:00 abstractendeavors env[2992447]:       genesis_signature: null,
2026-01-23T02:11:02.295338+00:00 abstractendeavors env[2992447]:       bonding_curve: null,
2026-01-23T02:11:02.295342+00:00 abstractendeavors env[2992447]:       associated_bonding_curve: null,
2026-01-23T02:11:02.295346+00:00 abstractendeavors env[2992447]:       program_id: null,
2026-01-23T02:11:02.295350+00:00 abstractendeavors env[2992447]:       seller_fee_basis_points: null,
2026-01-23T02:11:02.295353+00:00 abstractendeavors env[2992447]:       is_mutable: null,
2026-01-23T02:11:02.295357+00:00 abstractendeavors env[2992447]:       primary_sale_happened: null,
2026-01-23T02:11:02.295360+00:00 abstractendeavors env[2992447]:       token_standard: null,
2026-01-23T02:11:02.295364+00:00 abstractendeavors env[2992447]:       image: null,
2026-01-23T02:11:02.295369+00:00 abstractendeavors env[2992447]:       description: null,
2026-01-23T02:11:02.295372+00:00 abstractendeavors env[2992447]:       external_url: null,
2026-01-23T02:11:02.295376+00:00 abstractendeavors env[2992447]:       onchain_metadata: null,
2026-01-23T02:11:02.295384+00:00 abstractendeavors env[2992447]:       offchain_metadata: [Array],
2026-01-23T02:11:02.295388+00:00 abstractendeavors env[2992447]:       has_metadata: true,
2026-01-23T02:11:02.295393+00:00 abstractendeavors env[2992447]:       meta_created_at: null,
2026-01-23T02:11:02.295396+00:00 abstractendeavors env[2992447]:       created_at: 2026-01-20T17:47:10.802Z,
2026-01-23T02:11:02.295400+00:00 abstractendeavors env[2992447]:       updated_at: 2026-01-20T17:47:11.569Z,
2026-01-23T02:11:02.295404+00:00 abstractendeavors env[2992447]:       processed_at: null
2026-01-23T02:11:02.295407+00:00 abstractendeavors env[2992447]:     }
2026-01-23T02:11:02.295410+00:00 abstractendeavors env[2992447]:   }
2026-01-23T02:11:02.295412+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.295419+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.295422+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.295426+00:00 abstractendeavors env[2992447]:   message: 'metaDataCall recieved  {"mint":"6MCH7JHKtT889VqBSk1uKr4hL1s4ogekwivvKoJRCY12","bonding_curve":"EepFDswNQeVRTLKs2gp2YAeKUVpxMjJBBSSWzW719erx","associated_bonding_curve":"GSj76vRNReFPUBbBALMQLMdx8PjXg2Ub1buh6o7395sZ"}'
2026-01-23T02:11:02.295429+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.334600+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'txnEntry recieved  {"id":3049458}' }
2026-01-23T02:11:02.334620+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.334623+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.334627+00:00 abstractendeavors env[2992458]:   message: 'metaDataCall recieved  {"mint":"8K7EBnqSnFxHahxxeWrQw4awU7ZuBd6w9HbbQYgdpump","bonding_curve":"HA2Xx1fX7cC9bQV6hyGCreyQtkLgWcAWJS3An83gopiG","associated_bonding_curve":"Fq7RWjiw9C2j8yrJjH8AuVcW88mjdyaDATeNFpyfXhXt"}'
2026-01-23T02:11:02.334630+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.413594+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logIntake processed  3242732' }
2026-01-23T02:11:02.413622+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logIntake processed  3242728' }
2026-01-23T02:11:02.413629+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.413635+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.413641+00:00 abstractendeavors env[2992458]:   message: 'logIntake Sent  3242728 to logEntryQueue'
2026-01-23T02:11:02.413647+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.413652+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.413658+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.413663+00:00 abstractendeavors env[2992458]:   message: 'Queue handler',
2026-01-23T02:11:02.413669+00:00 abstractendeavors env[2992458]:   details: { queue: 'logIntake', result: 3242728 }
2026-01-23T02:11:02.413674+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.413689+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logIntake processed  3242733' }
2026-01-23T02:11:02.413695+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.413701+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.413706+00:00 abstractendeavors env[2992459]:   message: 'logIntake Sent  3242733 to logEntryQueue'
2026-01-23T02:11:02.413711+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.413719+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.413724+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.413730+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.413736+00:00 abstractendeavors env[2992459]:   details: { queue: 'logIntake', result: 3242733 }
2026-01-23T02:11:02.413742+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.413755+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.413761+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.413767+00:00 abstractendeavors env[2992446]:   message: 'logIntake Sent  3242732 to logEntryQueue'
2026-01-23T02:11:02.413773+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.413778+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.413783+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.413789+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:02.413795+00:00 abstractendeavors env[2992446]:   details: { queue: 'logIntake', result: 3242732 }
2026-01-23T02:11:02.413800+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.413815+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logEntry processed  3242587' }
2026-01-23T02:11:02.413821+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.413826+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.413832+00:00 abstractendeavors env[2992458]:   message: 'logEntry Sent  3242587 to txnEntryQueue'
2026-01-23T02:11:02.413837+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.413842+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.413848+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.413853+00:00 abstractendeavors env[2992458]:   message: 'Queue handler',
2026-01-23T02:11:02.413858+00:00 abstractendeavors env[2992458]:   details: { queue: 'logEntry', result: 3242587 }
2026-01-23T02:11:02.413864+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.413874+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry processed  3242596' }
2026-01-23T02:11:02.413886+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logEntry processed  3242575' }
2026-01-23T02:11:02.413909+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.413913+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.413917+00:00 abstractendeavors env[2992459]:   message: 'logEntry Sent  3242596 to txnEntryQueue'
2026-01-23T02:11:02.413920+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.413929+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logIntake processed  3242731' }
2026-01-23T02:11:02.413932+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.413936+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.413939+00:00 abstractendeavors env[2992446]:   message: 'logIntake Sent  3242731 to logEntryQueue'
2026-01-23T02:11:02.413943+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.413950+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.413953+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.413957+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.413960+00:00 abstractendeavors env[2992459]:   details: { queue: 'logEntry', result: 3242596 }
2026-01-23T02:11:02.413964+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.413972+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.413975+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.413979+00:00 abstractendeavors env[2992447]:   message: 'logEntry Sent  3242575 to txnEntryQueue'
2026-01-23T02:11:02.413983+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.413986+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.413990+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.413994+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:02.413998+00:00 abstractendeavors env[2992447]:   details: { queue: 'logEntry', result: 3242575 }
2026-01-23T02:11:02.414002+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.414009+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.414012+00:00 abstractendeavors env[2992446]:   logType: 'debug',
2026-01-23T02:11:02.414016+00:00 abstractendeavors env[2992446]:   message: 'Queue handler',
2026-01-23T02:11:02.414020+00:00 abstractendeavors env[2992446]:   details: { queue: 'logIntake', result: 3242731 }
2026-01-23T02:11:02.414023+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.414030+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logIntake processed  3242727' }
2026-01-23T02:11:02.414034+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.414038+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.414042+00:00 abstractendeavors env[2992459]:   message: 'logIntake Sent  3242727 to logEntryQueue'
2026-01-23T02:11:02.414046+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.414050+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.414054+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.414058+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.414062+00:00 abstractendeavors env[2992459]:   details: { queue: 'logIntake', result: 3242727 }
2026-01-23T02:11:02.414065+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.414072+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.414076+00:00 abstractendeavors env[2992458]:   function_name: 'processTxns',
2026-01-23T02:11:02.414079+00:00 abstractendeavors env[2992458]:   message: 'Transaction processing completed',
2026-01-23T02:11:02.414083+00:00 abstractendeavors env[2992458]:   details: {
2026-01-23T02:11:02.414087+00:00 abstractendeavors env[2992458]:     signature: '5XCKXgzXSsDM9EqV8C1xr1wLydfnEw2KYrHDguDU2cqDERqQm9Q7H8dEAPU73jBxf7mt8pyoKRm8w3bp6XaHQKQF',
2026-01-23T02:11:02.414091+00:00 abstractendeavors env[2992458]:     txn_id: undefined,
2026-01-23T02:11:02.414094+00:00 abstractendeavors env[2992458]:     pair_id: 52304,
2026-01-23T02:11:02.414098+00:00 abstractendeavors env[2992458]:     meta_id: 217175,
2026-01-23T02:11:02.414101+00:00 abstractendeavors env[2992458]:     log_id: 3049151
2026-01-23T02:11:02.414105+00:00 abstractendeavors env[2992458]:   },
2026-01-23T02:11:02.414109+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.414112+00:00 abstractendeavors env[2992458]:   logType: 'success'
2026-01-23T02:11:02.414116+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.414124+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'txnEntry processed  [object Object]' }
2026-01-23T02:11:02.414128+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.414131+00:00 abstractendeavors env[2992458]:   logType: 'debug',
2026-01-23T02:11:02.414135+00:00 abstractendeavors env[2992458]:   message: 'Queue handler',
2026-01-23T02:11:02.414139+00:00 abstractendeavors env[2992458]:   details: {
2026-01-23T02:11:02.414143+00:00 abstractendeavors env[2992458]:     queue: 'txnEntry',
2026-01-23T02:11:02.414147+00:00 abstractendeavors env[2992458]:     result: {
2026-01-23T02:11:02.414151+00:00 abstractendeavors env[2992458]:       signature: '5XCKXgzXSsDM9EqV8C1xr1wLydfnEw2KYrHDguDU2cqDERqQm9Q7H8dEAPU73jBxf7mt8pyoKRm8w3bp6XaHQKQF',
2026-01-23T02:11:02.414155+00:00 abstractendeavors env[2992458]:       meta_id: 217175,
2026-01-23T02:11:02.414159+00:00 abstractendeavors env[2992458]:       log_id: 3049151,
2026-01-23T02:11:02.414163+00:00 abstractendeavors env[2992458]:       pair_id: 52304,
2026-01-23T02:11:02.414167+00:00 abstractendeavors env[2992458]:       mint: 'E6MAyPJe3hqLHfK5mha5vwbi2TKFGUbriyn4tEe1pump',
2026-01-23T02:11:02.414171+00:00 abstractendeavors env[2992458]:       signatures: null,
2026-01-23T02:11:02.414175+00:00 abstractendeavors env[2992458]:       slot: 395279066,
2026-01-23T02:11:02.414179+00:00 abstractendeavors env[2992458]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.414182+00:00 abstractendeavors env[2992458]:       logs: [Array],
2026-01-23T02:11:02.414186+00:00 abstractendeavors env[2992458]:       tcns: [],
2026-01-23T02:11:02.414190+00:00 abstractendeavors env[2992458]:       sol_amount: 19600001n,
2026-01-23T02:11:02.414194+00:00 abstractendeavors env[2992458]:       token_amount: 208329309855n,
2026-01-23T02:11:02.414197+00:00 abstractendeavors env[2992458]:       is_buy: true,
2026-01-23T02:11:02.414201+00:00 abstractendeavors env[2992458]:       user: 'F2SsGGeGiDAyqhayraMo97R5ikinsVm6MgZyHSpHNq9e',
2026-01-23T02:11:02.414204+00:00 abstractendeavors env[2992458]:       timestamp: 1769121749n,
2026-01-23T02:11:02.414208+00:00 abstractendeavors env[2992458]:       virtual_sol_reserves: 55041552609n,
2026-01-23T02:11:02.414212+00:00 abstractendeavors env[2992458]:       virtual_token_reserves: 584830888452766n,
2026-01-23T02:11:02.414216+00:00 abstractendeavors env[2992458]:       real_sol_reserves: 25041552609n,
2026-01-23T02:11:02.414220+00:00 abstractendeavors env[2992458]:       real_token_reserves: 304930888452766n,
2026-01-23T02:11:02.414224+00:00 abstractendeavors env[2992458]:       fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.414228+00:00 abstractendeavors env[2992458]:       fee_basis_points: 95n,
2026-01-23T02:11:02.414232+00:00 abstractendeavors env[2992458]:       fee: 186201n,
2026-01-23T02:11:02.414235+00:00 abstractendeavors env[2992458]:       creator: 'FqTskkpwbtXGUxjPHtMu2wdTvTCWiSATcFHQ8vWG3msG',
2026-01-23T02:11:02.414239+00:00 abstractendeavors env[2992458]:       creator_fee_basis_points: 30n,
2026-01-23T02:11:02.414243+00:00 abstractendeavors env[2992458]:       creator_fee: 58801n,
2026-01-23T02:11:02.414246+00:00 abstractendeavors env[2992458]:       track_volume: false,
2026-01-23T02:11:02.414250+00:00 abstractendeavors env[2992458]:       total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.414254+00:00 abstractendeavors env[2992458]:       total_claimed_tokens: 0n,
2026-01-23T02:11:02.414258+00:00 abstractendeavors env[2992458]:       current_sol_volume: 0n,
2026-01-23T02:11:02.414262+00:00 abstractendeavors env[2992458]:       last_update_timestamp: 0n,
2026-01-23T02:11:02.414266+00:00 abstractendeavors env[2992458]:       ix_name: 'buy',
2026-01-23T02:11:02.414269+00:00 abstractendeavors env[2992458]:       mayhem_mode: false
2026-01-23T02:11:02.414273+00:00 abstractendeavors env[2992458]:     }
2026-01-23T02:11:02.414277+00:00 abstractendeavors env[2992458]:   }
2026-01-23T02:11:02.414280+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.414292+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logIntake processed  3242729' }
2026-01-23T02:11:02.414296+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.414299+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.414303+00:00 abstractendeavors env[2992459]:   message: 'logIntake Sent  3242729 to logEntryQueue'
2026-01-23T02:11:02.414307+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.414311+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.414314+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.414322+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.414328+00:00 abstractendeavors env[2992459]:   details: { queue: 'logIntake', result: 3242729 }
2026-01-23T02:11:02.414332+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.414336+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logIntake processed  3242730' }
2026-01-23T02:11:02.414339+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.414343+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.414346+00:00 abstractendeavors env[2992459]:   message: 'logIntake Sent  3242730 to logEntryQueue'
2026-01-23T02:11:02.414350+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.414353+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.414357+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.414360+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.414364+00:00 abstractendeavors env[2992459]:   details: { queue: 'logIntake', result: 3242730 }
2026-01-23T02:11:02.414368+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.414376+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.414380+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:02.414384+00:00 abstractendeavors env[2992458]:   message: 'meta_id',
2026-01-23T02:11:02.414387+00:00 abstractendeavors env[2992458]:   details: 217209,
2026-01-23T02:11:02.414391+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.414395+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:02.414398+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.414406+00:00 abstractendeavors env[2992446]: {
2026-01-23T02:11:02.414409+00:00 abstractendeavors env[2992446]:   function_name: 'getTcns',
2026-01-23T02:11:02.414413+00:00 abstractendeavors env[2992446]:   message: 'Error processing transaction log',
2026-01-23T02:11:02.414417+00:00 abstractendeavors env[2992446]:   details: {
2026-01-23T02:11:02.414421+00:00 abstractendeavors env[2992446]:     error: '"null value in column \\"user_address\\" of relation \\"transactions\\" violates not-null constraint"',
2026-01-23T02:11:02.414424+00:00 abstractendeavors env[2992446]:     invocation: {
2026-01-23T02:11:02.414428+00:00 abstractendeavors env[2992446]:       data: [Array],
2026-01-23T02:11:02.414431+00:00 abstractendeavors env[2992446]:       logs: [Array],
2026-01-23T02:11:02.414435+00:00 abstractendeavors env[2992446]:       depth: 0,
2026-01-23T02:11:02.414438+00:00 abstractendeavors env[2992446]:       compute: [Object],
2026-01-23T02:11:02.414442+00:00 abstractendeavors env[2992446]:       children: [Array],
2026-01-23T02:11:02.414445+00:00 abstractendeavors env[2992446]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.414449+00:00 abstractendeavors env[2992446]:       invocation_index: 7,
2026-01-23T02:11:02.414452+00:00 abstractendeavors env[2992446]:       reported_invocation: 1
2026-01-23T02:11:02.414456+00:00 abstractendeavors env[2992446]:     }
2026-01-23T02:11:02.414459+00:00 abstractendeavors env[2992446]:   },
2026-01-23T02:11:02.414463+00:00 abstractendeavors env[2992446]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.414467+00:00 abstractendeavors env[2992446]:   logType: 'error'
2026-01-23T02:11:02.414470+00:00 abstractendeavors env[2992446]: }
2026-01-23T02:11:02.414508+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.414513+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.414517+00:00 abstractendeavors env[2992459]:   message: 'Error processing transaction log',
2026-01-23T02:11:02.414521+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.414524+00:00 abstractendeavors env[2992459]:     error: '"null value in column \\"user_address\\" of relation \\"transactions\\" violates not-null constraint"',
2026-01-23T02:11:02.414528+00:00 abstractendeavors env[2992459]:     invocation: {
2026-01-23T02:11:02.414531+00:00 abstractendeavors env[2992459]:       data: [Array],
2026-01-23T02:11:02.414535+00:00 abstractendeavors env[2992459]:       logs: [Array],
2026-01-23T02:11:02.414539+00:00 abstractendeavors env[2992459]:       depth: 0,
2026-01-23T02:11:02.414547+00:00 abstractendeavors env[2992459]:       compute: [Object],
2026-01-23T02:11:02.414551+00:00 abstractendeavors env[2992459]:       children: [Array],
2026-01-23T02:11:02.414560+00:00 abstractendeavors env[2992459]:       program_id: '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P',
2026-01-23T02:11:02.414567+00:00 abstractendeavors env[2992459]:       invocation_index: 3,
2026-01-23T02:11:02.414571+00:00 abstractendeavors env[2992459]:       reported_invocation: 1
2026-01-23T02:11:02.414575+00:00 abstractendeavors env[2992459]:     }
2026-01-23T02:11:02.414579+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.414583+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.414587+00:00 abstractendeavors env[2992459]:   logType: 'error'
2026-01-23T02:11:02.414591+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.414673+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.414679+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.414683+00:00 abstractendeavors env[2992447]:   message: 'metaDataCall processed  [object Object]'
2026-01-23T02:11:02.414687+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.414695+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry recieved  {"id":3242728}' }
2026-01-23T02:11:02.414712+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.414717+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.414720+00:00 abstractendeavors env[2992447]:   message: 'Queue handler',
2026-01-23T02:11:02.414724+00:00 abstractendeavors env[2992447]:   details: {
2026-01-23T02:11:02.414729+00:00 abstractendeavors env[2992447]:     queue: 'metaDataCall',
2026-01-23T02:11:02.414733+00:00 abstractendeavors env[2992447]:     result: MetaDataRow {
2026-01-23T02:11:02.414738+00:00 abstractendeavors env[2992447]:       id: 54477,
2026-01-23T02:11:02.414742+00:00 abstractendeavors env[2992447]:       mint: 'CYjBQPKFqVGVLrQLvrHHATPzTrroKeVf5HaPvVQmpump',
2026-01-23T02:11:02.414747+00:00 abstractendeavors env[2992447]:       metadata_pda: null,
2026-01-23T02:11:02.414750+00:00 abstractendeavors env[2992447]:       update_authority: null,
2026-01-23T02:11:02.414754+00:00 abstractendeavors env[2992447]:       discriminator: null,
2026-01-23T02:11:02.414758+00:00 abstractendeavors env[2992447]:       name: null,
2026-01-23T02:11:02.414762+00:00 abstractendeavors env[2992447]:       symbol: null,
2026-01-23T02:11:02.414766+00:00 abstractendeavors env[2992447]:       uri: null,
2026-01-23T02:11:02.414770+00:00 abstractendeavors env[2992447]:       user_address: null,
2026-01-23T02:11:02.414773+00:00 abstractendeavors env[2992447]:       genesis_signature: null,
2026-01-23T02:11:02.414777+00:00 abstractendeavors env[2992447]:       bonding_curve: null,
2026-01-23T02:11:02.414782+00:00 abstractendeavors env[2992447]:       associated_bonding_curve: null,
2026-01-23T02:11:02.414786+00:00 abstractendeavors env[2992447]:       program_id: null,
2026-01-23T02:11:02.414790+00:00 abstractendeavors env[2992447]:       seller_fee_basis_points: null,
2026-01-23T02:11:02.414793+00:00 abstractendeavors env[2992447]:       is_mutable: null,
2026-01-23T02:11:02.414797+00:00 abstractendeavors env[2992447]:       primary_sale_happened: null,
2026-01-23T02:11:02.414801+00:00 abstractendeavors env[2992447]:       token_standard: null,
2026-01-23T02:11:02.414804+00:00 abstractendeavors env[2992447]:       image: null,
2026-01-23T02:11:02.414808+00:00 abstractendeavors env[2992447]:       description: null,
2026-01-23T02:11:02.414812+00:00 abstractendeavors env[2992447]:       external_url: null,
2026-01-23T02:11:02.414815+00:00 abstractendeavors env[2992447]:       onchain_metadata: null,
2026-01-23T02:11:02.414819+00:00 abstractendeavors env[2992447]:       offchain_metadata: [Array],
2026-01-23T02:11:02.414823+00:00 abstractendeavors env[2992447]:       has_metadata: true,
2026-01-23T02:11:02.414826+00:00 abstractendeavors env[2992447]:       meta_created_at: null,
2026-01-23T02:11:02.414829+00:00 abstractendeavors env[2992447]:       created_at: 2026-01-20T17:41:15.531Z,
2026-01-23T02:11:02.414833+00:00 abstractendeavors env[2992447]:       updated_at: 2026-01-20T17:41:15.729Z,
2026-01-23T02:11:02.414836+00:00 abstractendeavors env[2992447]:       processed_at: null
2026-01-23T02:11:02.414841+00:00 abstractendeavors env[2992447]:     }
2026-01-23T02:11:02.414845+00:00 abstractendeavors env[2992447]:   }
2026-01-23T02:11:02.414848+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.415008+00:00 abstractendeavors env[2992447]: { logType: 'debug', message: 'logEntry recieved  {"id":3242731}' }
2026-01-23T02:11:02.415015+00:00 abstractendeavors env[2992447]: {
2026-01-23T02:11:02.415018+00:00 abstractendeavors env[2992447]:   logType: 'debug',
2026-01-23T02:11:02.415023+00:00 abstractendeavors env[2992447]:   message: 'metaDataCall recieved  {"mint":"CYjBQPKFqVGVLrQLvrHHATPzTrroKeVf5HaPvVQmpump","bonding_curve":"2TDKkavTDVEcPXC7fS6i6UJs5nJ9em4io1KAcFTE1kLX","associated_bonding_curve":"AgZAK8Yf2h6GoJ2Qbba5HM3DCz81xUBGxTGny5gX7sLz"}'
2026-01-23T02:11:02.415028+00:00 abstractendeavors env[2992447]: }
2026-01-23T02:11:02.415037+00:00 abstractendeavors env[2992446]: { logType: 'debug', message: 'logEntry recieved  {"id":3242729}' }
2026-01-23T02:11:02.415045+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry processed  3242597' }
2026-01-23T02:11:02.415052+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.415057+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.415061+00:00 abstractendeavors env[2992459]:   message: 'logEntry Sent  3242597 to txnEntryQueue'
2026-01-23T02:11:02.415064+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.415070+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.415074+00:00 abstractendeavors env[2992459]:   logType: 'debug',
2026-01-23T02:11:02.415078+00:00 abstractendeavors env[2992459]:   message: 'Queue handler',
2026-01-23T02:11:02.415082+00:00 abstractendeavors env[2992459]:   details: { queue: 'logEntry', result: 3242597 }
2026-01-23T02:11:02.415087+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.415228+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.415232+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.415236+00:00 abstractendeavors env[2992459]:   message: 'meta_id',
2026-01-23T02:11:02.415239+00:00 abstractendeavors env[2992459]:   details: 217285,
2026-01-23T02:11:02.415243+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.415247+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.415250+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.415403+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.415408+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:02.415412+00:00 abstractendeavors env[2992458]:   message: 'meta_id',
2026-01-23T02:11:02.415415+00:00 abstractendeavors env[2992458]:   details: 216873,
2026-01-23T02:11:02.415419+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.415422+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:02.415426+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.416207+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416212+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.416215+00:00 abstractendeavors env[2992459]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.416219+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.416223+00:00 abstractendeavors env[2992459]:     signature: '3HzpVrGXw4QqfHRNAyKFZLRK7pRqidsTXxMcYQjjEUhGpAzAXmdWw6XCjM1oqdwsGy9B2WXbRvcbbQjLS1hSYaLv',
2026-01-23T02:11:02.416227+00:00 abstractendeavors env[2992459]:     slot: 395279095
2026-01-23T02:11:02.416230+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.416234+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.416238+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.416241+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416272+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416278+00:00 abstractendeavors env[2992459]:   mint: 'DmZVKmL9qhunaCv9f33U67L5sge14ktYjtvbMG9UH4FA',
2026-01-23T02:11:02.416282+00:00 abstractendeavors env[2992459]:   sol_amount: 35381164n,
2026-01-23T02:11:02.416286+00:00 abstractendeavors env[2992459]:   token_amount: 363832458776n,
2026-01-23T02:11:02.416290+00:00 abstractendeavors env[2992459]:   is_buy: false,
2026-01-23T02:11:02.416294+00:00 abstractendeavors env[2992459]:   user: '2ThyJUaubspM8sxzNYMbVi2rE2YRM9XbfoP46ijdp72p',
2026-01-23T02:11:02.416297+00:00 abstractendeavors env[2992459]:   timestamp: 1769121761n,
2026-01-23T02:11:02.416301+00:00 abstractendeavors env[2992459]:   virtual_sol_reserves: 55931762931n,
2026-01-23T02:11:02.416305+00:00 abstractendeavors env[2992459]:   virtual_token_reserves: 575522715680777n,
2026-01-23T02:11:02.416309+00:00 abstractendeavors env[2992459]:   real_sol_reserves: 25931762931n,
2026-01-23T02:11:02.416313+00:00 abstractendeavors env[2992459]:   real_token_reserves: 295622715680777n,
2026-01-23T02:11:02.416317+00:00 abstractendeavors env[2992459]:   fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.416326+00:00 abstractendeavors env[2992459]:   fee_basis_points: 95n,
2026-01-23T02:11:02.416330+00:00 abstractendeavors env[2992459]:   fee: 336122n,
2026-01-23T02:11:02.416335+00:00 abstractendeavors env[2992459]:   creator: 'bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa',
2026-01-23T02:11:02.416339+00:00 abstractendeavors env[2992459]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.416342+00:00 abstractendeavors env[2992459]:   creator_fee: 106144n,
2026-01-23T02:11:02.416345+00:00 abstractendeavors env[2992459]:   track_volume: false,
2026-01-23T02:11:02.416347+00:00 abstractendeavors env[2992459]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.416350+00:00 abstractendeavors env[2992459]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.416353+00:00 abstractendeavors env[2992459]:   current_sol_volume: 0n,
2026-01-23T02:11:02.416356+00:00 abstractendeavors env[2992459]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.416360+00:00 abstractendeavors env[2992459]:   ix_name: 'sell',
2026-01-23T02:11:02.416362+00:00 abstractendeavors env[2992459]:   mayhem_mode: false
2026-01-23T02:11:02.416365+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416373+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416377+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.416379+00:00 abstractendeavors env[2992459]:   message: 'decodedData',
2026-01-23T02:11:02.416382+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.416385+00:00 abstractendeavors env[2992459]:     mint: 'DmZVKmL9qhunaCv9f33U67L5sge14ktYjtvbMG9UH4FA',
2026-01-23T02:11:02.416388+00:00 abstractendeavors env[2992459]:     sol_amount: 35381164n,
2026-01-23T02:11:02.416391+00:00 abstractendeavors env[2992459]:     token_amount: 363832458776n,
2026-01-23T02:11:02.416393+00:00 abstractendeavors env[2992459]:     is_buy: false,
2026-01-23T02:11:02.416396+00:00 abstractendeavors env[2992459]:     user: '2ThyJUaubspM8sxzNYMbVi2rE2YRM9XbfoP46ijdp72p',
2026-01-23T02:11:02.416399+00:00 abstractendeavors env[2992459]:     timestamp: 1769121761n,
2026-01-23T02:11:02.416403+00:00 abstractendeavors env[2992459]:     virtual_sol_reserves: 55931762931n,
2026-01-23T02:11:02.416406+00:00 abstractendeavors env[2992459]:     virtual_token_reserves: 575522715680777n,
2026-01-23T02:11:02.416409+00:00 abstractendeavors env[2992459]:     real_sol_reserves: 25931762931n,
2026-01-23T02:11:02.416411+00:00 abstractendeavors env[2992459]:     real_token_reserves: 295622715680777n,
2026-01-23T02:11:02.416414+00:00 abstractendeavors env[2992459]:     fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.416417+00:00 abstractendeavors env[2992459]:     fee_basis_points: 95n,
2026-01-23T02:11:02.416421+00:00 abstractendeavors env[2992459]:     fee: 336122n,
2026-01-23T02:11:02.416424+00:00 abstractendeavors env[2992459]:     creator: 'bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa',
2026-01-23T02:11:02.416426+00:00 abstractendeavors env[2992459]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.416429+00:00 abstractendeavors env[2992459]:     creator_fee: 106144n,
2026-01-23T02:11:02.416432+00:00 abstractendeavors env[2992459]:     track_volume: false,
2026-01-23T02:11:02.416435+00:00 abstractendeavors env[2992459]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.416438+00:00 abstractendeavors env[2992459]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.416441+00:00 abstractendeavors env[2992459]:     current_sol_volume: 0n,
2026-01-23T02:11:02.416444+00:00 abstractendeavors env[2992459]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.416446+00:00 abstractendeavors env[2992459]:     ix_name: 'sell',
2026-01-23T02:11:02.416449+00:00 abstractendeavors env[2992459]:     mayhem_mode: false
2026-01-23T02:11:02.416452+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.416455+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.416457+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.416461+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416464+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry recieved  {"id":3242733}' }
2026-01-23T02:11:02.416467+00:00 abstractendeavors env[2992459]: { logType: 'debug', message: 'logEntry recieved  {"id":3242730}' }
2026-01-23T02:11:02.416472+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416476+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.416478+00:00 abstractendeavors env[2992459]:   message: 'pairData_',
2026-01-23T02:11:02.416481+00:00 abstractendeavors env[2992459]:   details: null,
2026-01-23T02:11:02.416484+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.416486+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.416489+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416494+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416497+00:00 abstractendeavors env[2992459]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:02.416500+00:00 abstractendeavors env[2992459]:   message: 'processMetaData',
2026-01-23T02:11:02.416503+00:00 abstractendeavors env[2992459]:   details: '4kzEJ9EfhY9cWuUzsatCrR4AeZbqxCRz2HrRLtX8D38pLBMXJkj3vzDMnoTe6MwdQchGNrpM5vP5BMT9JarqtBKt',
2026-01-23T02:11:02.416506+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.416509+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.416511+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416584+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416591+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.416594+00:00 abstractendeavors env[2992459]:   message: 'pairData_',
2026-01-23T02:11:02.416598+00:00 abstractendeavors env[2992459]:   details: null,
2026-01-23T02:11:02.416602+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.416609+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.416615+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416622+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416626+00:00 abstractendeavors env[2992459]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:02.416629+00:00 abstractendeavors env[2992459]:   message: 'processMetaData',
2026-01-23T02:11:02.416632+00:00 abstractendeavors env[2992459]:   details: '2u2jhrWtaw6xMmgHVtXx6qTHLqU4Xm56yg6q1rBVqBNXPgVefrTHeqXQpYZofVUxc6YzHuLsjYJ4uKM4EqXNwyYh',
2026-01-23T02:11:02.416635+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.416639+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.416642+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416657+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416660+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.416663+00:00 abstractendeavors env[2992459]:   message: 'pairData_',
2026-01-23T02:11:02.416666+00:00 abstractendeavors env[2992459]:   details: null,
2026-01-23T02:11:02.416669+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.416672+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.416675+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416681+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416684+00:00 abstractendeavors env[2992459]:   function_name: 'getOrProcessMetaId',
2026-01-23T02:11:02.416687+00:00 abstractendeavors env[2992459]:   message: 'processMetaData',
2026-01-23T02:11:02.416690+00:00 abstractendeavors env[2992459]:   details: '2p6s1hNsm3M8zmVTiRsLzpAq3RXvJBv4EAyPh7f95gyZV8gT5jioEMA5wgmHgDtxReHhhCDMYkpwj3LKh9TWXxM6',
2026-01-23T02:11:02.416693+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.416696+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.416700+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416795+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416798+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.416801+00:00 abstractendeavors env[2992459]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.416804+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.416807+00:00 abstractendeavors env[2992459]:     signature: '4feAHfw2hZLc6eAamoZDZ9ZLSPSsY6a8mMDkndC5o1RXwBDpzh3mEm9QdotA4QKET8KtCsgAyQQsbu8n1DL27cht',
2026-01-23T02:11:02.416809+00:00 abstractendeavors env[2992459]:     slot: 395279086
2026-01-23T02:11:02.416812+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.416815+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.416818+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.416822+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416829+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logEntry recieved  {"id":3242732}' }
2026-01-23T02:11:02.416833+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'txnEntry recieved  {"id":3049465}' }
2026-01-23T02:11:02.416836+00:00 abstractendeavors env[2992458]: { logType: 'debug', message: 'logEntry recieved  {"id":3242727}' }
2026-01-23T02:11:02.416852+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416855+00:00 abstractendeavors env[2992459]:   mint: 'DmZVKmL9qhunaCv9f33U67L5sge14ktYjtvbMG9UH4FA',
2026-01-23T02:11:02.416858+00:00 abstractendeavors env[2992459]:   sol_amount: 48888888n,
2026-01-23T02:11:02.416860+00:00 abstractendeavors env[2992459]:   token_amount: 529957667275n,
2026-01-23T02:11:02.416863+00:00 abstractendeavors env[2992459]:   is_buy: true,
2026-01-23T02:11:02.416866+00:00 abstractendeavors env[2992459]:   user: 'H2uywkXuTLSJDDtc6jKC9KpgZtqn24MM648SDd8bqUCs',
2026-01-23T02:11:02.416870+00:00 abstractendeavors env[2992459]:   timestamp: 1769121758n,
2026-01-23T02:11:02.416873+00:00 abstractendeavors env[2992459]:   virtual_sol_reserves: 54517984565n,
2026-01-23T02:11:02.416876+00:00 abstractendeavors env[2992459]:   virtual_token_reserves: 590447360627501n,
2026-01-23T02:11:02.416879+00:00 abstractendeavors env[2992459]:   real_sol_reserves: 24517984565n,
2026-01-23T02:11:02.416882+00:00 abstractendeavors env[2992459]:   real_token_reserves: 310547360627501n,
2026-01-23T02:11:02.416885+00:00 abstractendeavors env[2992459]:   fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.416889+00:00 abstractendeavors env[2992459]:   fee_basis_points: 95n,
2026-01-23T02:11:02.416891+00:00 abstractendeavors env[2992459]:   fee: 464445n,
2026-01-23T02:11:02.416894+00:00 abstractendeavors env[2992459]:   creator: 'bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa',
2026-01-23T02:11:02.416897+00:00 abstractendeavors env[2992459]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.416900+00:00 abstractendeavors env[2992459]:   creator_fee: 146667n,
2026-01-23T02:11:02.416903+00:00 abstractendeavors env[2992459]:   track_volume: false,
2026-01-23T02:11:02.416907+00:00 abstractendeavors env[2992459]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.416909+00:00 abstractendeavors env[2992459]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.416912+00:00 abstractendeavors env[2992459]:   current_sol_volume: 0n,
2026-01-23T02:11:02.416915+00:00 abstractendeavors env[2992459]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.416918+00:00 abstractendeavors env[2992459]:   ix_name: 'buy',
2026-01-23T02:11:02.416921+00:00 abstractendeavors env[2992459]:   mayhem_mode: false
2026-01-23T02:11:02.416925+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.416930+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.416933+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.416936+00:00 abstractendeavors env[2992459]:   message: 'decodedData',
2026-01-23T02:11:02.416939+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.416942+00:00 abstractendeavors env[2992459]:     mint: 'DmZVKmL9qhunaCv9f33U67L5sge14ktYjtvbMG9UH4FA',
2026-01-23T02:11:02.416944+00:00 abstractendeavors env[2992459]:     sol_amount: 48888888n,
2026-01-23T02:11:02.416947+00:00 abstractendeavors env[2992459]:     token_amount: 529957667275n,
2026-01-23T02:11:02.416950+00:00 abstractendeavors env[2992459]:     is_buy: true,
2026-01-23T02:11:02.416954+00:00 abstractendeavors env[2992459]:     user: 'H2uywkXuTLSJDDtc6jKC9KpgZtqn24MM648SDd8bqUCs',
2026-01-23T02:11:02.416957+00:00 abstractendeavors env[2992459]:     timestamp: 1769121758n,
2026-01-23T02:11:02.416960+00:00 abstractendeavors env[2992459]:     virtual_sol_reserves: 54517984565n,
2026-01-23T02:11:02.416963+00:00 abstractendeavors env[2992459]:     virtual_token_reserves: 590447360627501n,
2026-01-23T02:11:02.416965+00:00 abstractendeavors env[2992459]:     real_sol_reserves: 24517984565n,
2026-01-23T02:11:02.416970+00:00 abstractendeavors env[2992459]:     real_token_reserves: 310547360627501n,
2026-01-23T02:11:02.416972+00:00 abstractendeavors env[2992459]:     fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.416975+00:00 abstractendeavors env[2992459]:     fee_basis_points: 95n,
2026-01-23T02:11:02.416978+00:00 abstractendeavors env[2992459]:     fee: 464445n,
2026-01-23T02:11:02.416981+00:00 abstractendeavors env[2992459]:     creator: 'bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa',
2026-01-23T02:11:02.416984+00:00 abstractendeavors env[2992459]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.416988+00:00 abstractendeavors env[2992459]:     creator_fee: 146667n,
2026-01-23T02:11:02.416990+00:00 abstractendeavors env[2992459]:     track_volume: false,
2026-01-23T02:11:02.416993+00:00 abstractendeavors env[2992459]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.416996+00:00 abstractendeavors env[2992459]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.417000+00:00 abstractendeavors env[2992459]:     current_sol_volume: 0n,
2026-01-23T02:11:02.417003+00:00 abstractendeavors env[2992459]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.417006+00:00 abstractendeavors env[2992459]:     ix_name: 'buy',
2026-01-23T02:11:02.417008+00:00 abstractendeavors env[2992459]:     mayhem_mode: false
2026-01-23T02:11:02.417011+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.417014+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.417017+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.417020+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.417025+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.417028+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:02.417031+00:00 abstractendeavors env[2992458]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.417034+00:00 abstractendeavors env[2992458]:   details: {
2026-01-23T02:11:02.417036+00:00 abstractendeavors env[2992458]:     signature: 'm7cFG3gP7qApwVSB2DgY8Y8NSxbXRTZdtnpJkpEbebbV3Dyuhfe628A4PRnSs4gWDJpdp5smqCCbM7RjK97Scdf',
2026-01-23T02:11:02.417039+00:00 abstractendeavors env[2992458]:     slot: 395279087
2026-01-23T02:11:02.417042+00:00 abstractendeavors env[2992458]:   },
2026-01-23T02:11:02.417046+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.417049+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:02.417052+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.417059+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.417063+00:00 abstractendeavors env[2992458]:   mint: 'DmZVKmL9qhunaCv9f33U67L5sge14ktYjtvbMG9UH4FA',
2026-01-23T02:11:02.417067+00:00 abstractendeavors env[2992458]:   sol_amount: 368460216n,
2026-01-23T02:11:02.417071+00:00 abstractendeavors env[2992458]:   token_amount: 4017696643414n,
2026-01-23T02:11:02.417075+00:00 abstractendeavors env[2992458]:   is_buy: false,
2026-01-23T02:11:02.417079+00:00 abstractendeavors env[2992458]:   user: 'HuvyEhJj2Utm2Aojcpdn78JfYx9cQxPsusG2BQdHjo2u',
2026-01-23T02:11:02.417081+00:00 abstractendeavors env[2992458]:   timestamp: 1769121758n,
2026-01-23T02:11:02.417084+00:00 abstractendeavors env[2992458]:   virtual_sol_reserves: 54149524349n,
2026-01-23T02:11:02.417087+00:00 abstractendeavors env[2992458]:   virtual_token_reserves: 594465057270915n,
2026-01-23T02:11:02.417090+00:00 abstractendeavors env[2992458]:   real_sol_reserves: 24149524349n,
2026-01-23T02:11:02.417092+00:00 abstractendeavors env[2992458]:   real_token_reserves: 314565057270915n,
2026-01-23T02:11:02.417095+00:00 abstractendeavors env[2992458]:   fee_recipient: 'CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM',
2026-01-23T02:11:02.417098+00:00 abstractendeavors env[2992458]:   fee_basis_points: 95n,
2026-01-23T02:11:02.417101+00:00 abstractendeavors env[2992458]:   fee: 3500373n,
2026-01-23T02:11:02.417104+00:00 abstractendeavors env[2992458]:   creator: 'bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa',
2026-01-23T02:11:02.417106+00:00 abstractendeavors env[2992458]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.417109+00:00 abstractendeavors env[2992458]:   creator_fee: 1105381n,
2026-01-23T02:11:02.417112+00:00 abstractendeavors env[2992458]:   track_volume: false,
2026-01-23T02:11:02.417115+00:00 abstractendeavors env[2992458]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.417118+00:00 abstractendeavors env[2992458]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.417120+00:00 abstractendeavors env[2992458]:   current_sol_volume: 0n,
2026-01-23T02:11:02.417123+00:00 abstractendeavors env[2992458]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.417126+00:00 abstractendeavors env[2992458]:   ix_name: 'sell',
2026-01-23T02:11:02.417129+00:00 abstractendeavors env[2992458]:   mayhem_mode: false
2026-01-23T02:11:02.417133+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.417141+00:00 abstractendeavors env[2992458]: {
2026-01-23T02:11:02.417145+00:00 abstractendeavors env[2992458]:   function_name: 'getTcns',
2026-01-23T02:11:02.417148+00:00 abstractendeavors env[2992458]:   message: 'decodedData',
2026-01-23T02:11:02.417151+00:00 abstractendeavors env[2992458]:   details: {
2026-01-23T02:11:02.417154+00:00 abstractendeavors env[2992458]:     mint: 'DmZVKmL9qhunaCv9f33U67L5sge14ktYjtvbMG9UH4FA',
2026-01-23T02:11:02.417157+00:00 abstractendeavors env[2992458]:     sol_amount: 368460216n,
2026-01-23T02:11:02.417160+00:00 abstractendeavors env[2992458]:     token_amount: 4017696643414n,
2026-01-23T02:11:02.417162+00:00 abstractendeavors env[2992458]:     is_buy: false,
2026-01-23T02:11:02.417165+00:00 abstractendeavors env[2992458]:     user: 'HuvyEhJj2Utm2Aojcpdn78JfYx9cQxPsusG2BQdHjo2u',
2026-01-23T02:11:02.417168+00:00 abstractendeavors env[2992458]:     timestamp: 1769121758n,
2026-01-23T02:11:02.417171+00:00 abstractendeavors env[2992458]:     virtual_sol_reserves: 54149524349n,
2026-01-23T02:11:02.417174+00:00 abstractendeavors env[2992458]:     virtual_token_reserves: 594465057270915n,
2026-01-23T02:11:02.417176+00:00 abstractendeavors env[2992458]:     real_sol_reserves: 24149524349n,
2026-01-23T02:11:02.417179+00:00 abstractendeavors env[2992458]:     real_token_reserves: 314565057270915n,
2026-01-23T02:11:02.417182+00:00 abstractendeavors env[2992458]:     fee_recipient: 'CebN5WGQ4jvEPvsVU4EoHEpgzq1VV7AbicfhtW4xC9iM',
2026-01-23T02:11:02.417185+00:00 abstractendeavors env[2992458]:     fee_basis_points: 95n,
2026-01-23T02:11:02.417188+00:00 abstractendeavors env[2992458]:     fee: 3500373n,
2026-01-23T02:11:02.417190+00:00 abstractendeavors env[2992458]:     creator: 'bwamJzztZsepfkteWRChggmXuiiCQvpLqPietdNfSXa',
2026-01-23T02:11:02.417193+00:00 abstractendeavors env[2992458]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.417196+00:00 abstractendeavors env[2992458]:     creator_fee: 1105381n,
2026-01-23T02:11:02.417199+00:00 abstractendeavors env[2992458]:     track_volume: false,
2026-01-23T02:11:02.417202+00:00 abstractendeavors env[2992458]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.417205+00:00 abstractendeavors env[2992458]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.417207+00:00 abstractendeavors env[2992458]:     current_sol_volume: 0n,
2026-01-23T02:11:02.417210+00:00 abstractendeavors env[2992458]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.417213+00:00 abstractendeavors env[2992458]:     ix_name: 'sell',
2026-01-23T02:11:02.417217+00:00 abstractendeavors env[2992458]:     mayhem_mode: false
2026-01-23T02:11:02.417222+00:00 abstractendeavors env[2992458]:   },
2026-01-23T02:11:02.417226+00:00 abstractendeavors env[2992458]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.417230+00:00 abstractendeavors env[2992458]:   logType: 'processing'
2026-01-23T02:11:02.417234+00:00 abstractendeavors env[2992458]: }
2026-01-23T02:11:02.417243+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.417248+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.417252+00:00 abstractendeavors env[2992459]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.417256+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.417260+00:00 abstractendeavors env[2992459]:     signature: '36DQscKQnCKdQWCfxDxUSnXr6veGfjMMUc6QeMkYwcwepNwDkbYREop3CAUK8Hir4rZYFJp2GZtf6zGGLnWdGBmx',
2026-01-23T02:11:02.417264+00:00 abstractendeavors env[2992459]:     slot: 395279105
2026-01-23T02:11:02.417268+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.417271+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.417275+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.417278+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.417282+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.417286+00:00 abstractendeavors env[2992459]:   mint: 'jwH1Trdiv5fHG2xJ6LpZJKH3XawLkohCgvArqr1pump',
2026-01-23T02:11:02.417290+00:00 abstractendeavors env[2992459]:   sol_amount: 700010746n,
2026-01-23T02:11:02.417294+00:00 abstractendeavors env[2992459]:   token_amount: 12155286778082n,
2026-01-23T02:11:02.417299+00:00 abstractendeavors env[2992459]:   is_buy: false,
2026-01-23T02:11:02.417303+00:00 abstractendeavors env[2992459]:   user: '5JgpKFiFP9M8jffMNiZsoL6hqgrAYFf9Kv3kWeYcqxFB',
2026-01-23T02:11:02.417307+00:00 abstractendeavors env[2992459]:   timestamp: 1769121764n,
2026-01-23T02:11:02.417311+00:00 abstractendeavors env[2992459]:   virtual_sol_reserves: 42707075885n,
2026-01-23T02:11:02.417315+00:00 abstractendeavors env[2992459]:   virtual_token_reserves: 753739266077831n,
2026-01-23T02:11:02.417322+00:00 abstractendeavors env[2992459]:   real_sol_reserves: 12707075885n,
2026-01-23T02:11:02.417326+00:00 abstractendeavors env[2992459]:   real_token_reserves: 473839266077831n,
2026-01-23T02:11:02.417330+00:00 abstractendeavors env[2992459]:   fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.417334+00:00 abstractendeavors env[2992459]:   fee_basis_points: 95n,
2026-01-23T02:11:02.417338+00:00 abstractendeavors env[2992459]:   fee: 6650103n,
2026-01-23T02:11:02.417342+00:00 abstractendeavors env[2992459]:   creator: 'D1Hm8z43y4kMzG7Bhe1cmLrbwKPdQj8JzDzZ2nD7XhHy',
2026-01-23T02:11:02.417346+00:00 abstractendeavors env[2992459]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.417350+00:00 abstractendeavors env[2992459]:   creator_fee: 2100033n,
2026-01-23T02:11:02.417355+00:00 abstractendeavors env[2992459]:   track_volume: false,
2026-01-23T02:11:02.417359+00:00 abstractendeavors env[2992459]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.417362+00:00 abstractendeavors env[2992459]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.417365+00:00 abstractendeavors env[2992459]:   current_sol_volume: 0n,
2026-01-23T02:11:02.417368+00:00 abstractendeavors env[2992459]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.417371+00:00 abstractendeavors env[2992459]:   ix_name: 'sell',
2026-01-23T02:11:02.417374+00:00 abstractendeavors env[2992459]:   mayhem_mode: false
2026-01-23T02:11:02.417377+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.417380+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.417384+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.417389+00:00 abstractendeavors env[2992459]:   message: 'decodedData',
2026-01-23T02:11:02.417392+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.417397+00:00 abstractendeavors env[2992459]:     mint: 'jwH1Trdiv5fHG2xJ6LpZJKH3XawLkohCgvArqr1pump',
2026-01-23T02:11:02.417401+00:00 abstractendeavors env[2992459]:     sol_amount: 700010746n,
2026-01-23T02:11:02.417404+00:00 abstractendeavors env[2992459]:     token_amount: 12155286778082n,
2026-01-23T02:11:02.417408+00:00 abstractendeavors env[2992459]:     is_buy: false,
2026-01-23T02:11:02.417411+00:00 abstractendeavors env[2992459]:     user: '5JgpKFiFP9M8jffMNiZsoL6hqgrAYFf9Kv3kWeYcqxFB',
2026-01-23T02:11:02.417413+00:00 abstractendeavors env[2992459]:     timestamp: 1769121764n,
2026-01-23T02:11:02.417416+00:00 abstractendeavors env[2992459]:     virtual_sol_reserves: 42707075885n,
2026-01-23T02:11:02.417419+00:00 abstractendeavors env[2992459]:     virtual_token_reserves: 753739266077831n,
2026-01-23T02:11:02.417423+00:00 abstractendeavors env[2992459]:     real_sol_reserves: 12707075885n,
2026-01-23T02:11:02.417426+00:00 abstractendeavors env[2992459]:     real_token_reserves: 473839266077831n,
2026-01-23T02:11:02.417429+00:00 abstractendeavors env[2992459]:     fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.417431+00:00 abstractendeavors env[2992459]:     fee_basis_points: 95n,
2026-01-23T02:11:02.417434+00:00 abstractendeavors env[2992459]:     fee: 6650103n,
2026-01-23T02:11:02.417437+00:00 abstractendeavors env[2992459]:     creator: 'D1Hm8z43y4kMzG7Bhe1cmLrbwKPdQj8JzDzZ2nD7XhHy',
2026-01-23T02:11:02.417441+00:00 abstractendeavors env[2992459]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.417444+00:00 abstractendeavors env[2992459]:     creator_fee: 2100033n,
2026-01-23T02:11:02.417447+00:00 abstractendeavors env[2992459]:     track_volume: false,
2026-01-23T02:11:02.417450+00:00 abstractendeavors env[2992459]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.417452+00:00 abstractendeavors env[2992459]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.417456+00:00 abstractendeavors env[2992459]:     current_sol_volume: 0n,
2026-01-23T02:11:02.417460+00:00 abstractendeavors env[2992459]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.417464+00:00 abstractendeavors env[2992459]:     ix_name: 'sell',
2026-01-23T02:11:02.417469+00:00 abstractendeavors env[2992459]:     mayhem_mode: false
2026-01-23T02:11:02.417473+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.417477+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.417481+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.417486+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.417496+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.417500+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.417504+00:00 abstractendeavors env[2992459]:   message: 'Processing transaction logs',
2026-01-23T02:11:02.417508+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.417512+00:00 abstractendeavors env[2992459]:     signature: '47Pb2fpSYso6vsUD8xkmwWoM3T69uTgFnoFsf67YqkoA1CyPsbbh7NzuqaWEZbK4NyQGMrggW9nhHde9JpHhvpLW',
2026-01-23T02:11:02.417516+00:00 abstractendeavors env[2992459]:     slot: 395279105
2026-01-23T02:11:02.417520+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.417525+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.417528+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.417532+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.417536+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.417540+00:00 abstractendeavors env[2992459]:   mint: 'AyjzJpws3CJ4aQxVBz6tLZKvo3KnULWHbLbZYh56pump',
2026-01-23T02:11:02.417544+00:00 abstractendeavors env[2992459]:   sol_amount: 987140447n,
2026-01-23T02:11:02.417549+00:00 abstractendeavors env[2992459]:   token_amount: 16620611261263n,
2026-01-23T02:11:02.417553+00:00 abstractendeavors env[2992459]:   is_buy: true,
2026-01-23T02:11:02.417557+00:00 abstractendeavors env[2992459]:   user: 'Edp1o6EkX9VKuzcM9YcxtYvfmUBYWPPuWpCQhbFEy69k',
2026-01-23T02:11:02.417561+00:00 abstractendeavors env[2992459]:   timestamp: 1769121764n,
2026-01-23T02:11:02.417566+00:00 abstractendeavors env[2992459]:   virtual_sol_reserves: 44221018387n,
2026-01-23T02:11:02.417570+00:00 abstractendeavors env[2992459]:   virtual_token_reserves: 727934389418896n,
2026-01-23T02:11:02.417574+00:00 abstractendeavors env[2992459]:   real_sol_reserves: 14221018387n,
2026-01-23T02:11:02.417578+00:00 abstractendeavors env[2992459]:   real_token_reserves: 448034389418896n,
2026-01-23T02:11:02.417582+00:00 abstractendeavors env[2992459]:   fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.417586+00:00 abstractendeavors env[2992459]:   fee_basis_points: 95n,
2026-01-23T02:11:02.417590+00:00 abstractendeavors env[2992459]:   fee: 9377835n,
2026-01-23T02:11:02.417593+00:00 abstractendeavors env[2992459]:   creator: '3y3QB64kViX7UKtFWbuGApqUaqd2Nc5mHEw2UP2Nm55B',
2026-01-23T02:11:02.417597+00:00 abstractendeavors env[2992459]:   creator_fee_basis_points: 30n,
2026-01-23T02:11:02.417601+00:00 abstractendeavors env[2992459]:   creator_fee: 2961422n,
2026-01-23T02:11:02.417605+00:00 abstractendeavors env[2992459]:   track_volume: false,
2026-01-23T02:11:02.417609+00:00 abstractendeavors env[2992459]:   total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.417614+00:00 abstractendeavors env[2992459]:   total_claimed_tokens: 0n,
2026-01-23T02:11:02.417620+00:00 abstractendeavors env[2992459]:   current_sol_volume: 0n,
2026-01-23T02:11:02.417624+00:00 abstractendeavors env[2992459]:   last_update_timestamp: 0n,
2026-01-23T02:11:02.417628+00:00 abstractendeavors env[2992459]:   ix_name: 'buy',
2026-01-23T02:11:02.417632+00:00 abstractendeavors env[2992459]:   mayhem_mode: false
2026-01-23T02:11:02.417637+00:00 abstractendeavors env[2992459]: }
2026-01-23T02:11:02.417641+00:00 abstractendeavors env[2992459]: {
2026-01-23T02:11:02.417646+00:00 abstractendeavors env[2992459]:   function_name: 'getTcns',
2026-01-23T02:11:02.417649+00:00 abstractendeavors env[2992459]:   message: 'decodedData',
2026-01-23T02:11:02.417653+00:00 abstractendeavors env[2992459]:   details: {
2026-01-23T02:11:02.417657+00:00 abstractendeavors env[2992459]:     mint: 'AyjzJpws3CJ4aQxVBz6tLZKvo3KnULWHbLbZYh56pump',
2026-01-23T02:11:02.417661+00:00 abstractendeavors env[2992459]:     sol_amount: 987140447n,
2026-01-23T02:11:02.417665+00:00 abstractendeavors env[2992459]:     token_amount: 16620611261263n,
2026-01-23T02:11:02.417668+00:00 abstractendeavors env[2992459]:     is_buy: true,
2026-01-23T02:11:02.417674+00:00 abstractendeavors env[2992459]:     user: 'Edp1o6EkX9VKuzcM9YcxtYvfmUBYWPPuWpCQhbFEy69k',
2026-01-23T02:11:02.417677+00:00 abstractendeavors env[2992459]:     timestamp: 1769121764n,
2026-01-23T02:11:02.417682+00:00 abstractendeavors env[2992459]:     virtual_sol_reserves: 44221018387n,
2026-01-23T02:11:02.417685+00:00 abstractendeavors env[2992459]:     virtual_token_reserves: 727934389418896n,
2026-01-23T02:11:02.417690+00:00 abstractendeavors env[2992459]:     real_sol_reserves: 14221018387n,
2026-01-23T02:11:02.417694+00:00 abstractendeavors env[2992459]:     real_token_reserves: 448034389418896n,
2026-01-23T02:11:02.417697+00:00 abstractendeavors env[2992459]:     fee_recipient: '62qc2CNXwrYqQScmEdiZFFAnJR262PxWEuNQtxfafNgV',
2026-01-23T02:11:02.417701+00:00 abstractendeavors env[2992459]:     fee_basis_points: 95n,
2026-01-23T02:11:02.417705+00:00 abstractendeavors env[2992459]:     fee: 9377835n,
2026-01-23T02:11:02.417709+00:00 abstractendeavors env[2992459]:     creator: '3y3QB64kViX7UKtFWbuGApqUaqd2Nc5mHEw2UP2Nm55B',
2026-01-23T02:11:02.417713+00:00 abstractendeavors env[2992459]:     creator_fee_basis_points: 30n,
2026-01-23T02:11:02.417716+00:00 abstractendeavors env[2992459]:     creator_fee: 2961422n,
2026-01-23T02:11:02.417720+00:00 abstractendeavors env[2992459]:     track_volume: false,
2026-01-23T02:11:02.417724+00:00 abstractendeavors env[2992459]:     total_unclaimed_tokens: 0n,
2026-01-23T02:11:02.417728+00:00 abstractendeavors env[2992459]:     total_claimed_tokens: 0n,
2026-01-23T02:11:02.417732+00:00 abstractendeavors env[2992459]:     current_sol_volume: 0n,
2026-01-23T02:11:02.417736+00:00 abstractendeavors env[2992459]:     last_update_timestamp: 0n,
2026-01-23T02:11:02.417740+00:00 abstractendeavors env[2992459]:     ix_name: 'buy',
2026-01-23T02:11:02.417744+00:00 abstractendeavors env[2992459]:     mayhem_mode: false
2026-01-23T02:11:02.417747+00:00 abstractendeavors env[2992459]:   },
2026-01-23T02:11:02.417750+00:00 abstractendeavors env[2992459]:   file_location: 'src/pipeline/bootstrap/processTxns.ts',
2026-01-23T02:11:02.417753+00:00 abstractendeavors env[2992459]:   logType: 'processing'
2026-01-23T02:11:02.417756+00:00 abstractendeavors env[2992459]: }
"""
import json
from abstract_utilities import *
counts = {"}":0,"{":0}
def check_counts(char):
    num = counts.get(char)
    if num !=None:
        counts[char]+=1
        total_count = 0
        count_values = list(counts.values())
        for count in count_values:
            total_count+=count
        if total_count != 0 and total_count/2 == count_values[0]:
            return True
    return False
def make_quotes(line):
    line = eatAll(line,' ')
    if not line.startswith('}') and not line.startswith('{'):
        key = line.split(':')[0]
        value = line.split(':')[-1]
        value = eatAll(value,' ')
        if value.startswith('false'):
            value = 'False'+value[len('false'):]
        if value.startswith('true'):
            value = 'True'+value[len('true'):]
        if value.startswith('null'):
            value = 'None'+value[len('null'):]   
        return f'"{key}":{value}'
    return line 
all_contents = [[]]
for text in texts.split('\n'):
    content = text.split(']: ')[-1]
    all_contents[-1].append(make_quotes(content))
    for char in content:
        if check_counts(char):
            obj = ''.join(all_contents[-1]).replace('{ ','{').replace(': ',':').replace('":',':').replace("':",':').replace(' }','}').replace(', ',',').replace('{"','{').replace("{'",'{').replace("'}",'}').replace('"}','}').replace('{','{"').replace('}','"}').replace(':','":').replace(":'",':"').replace(",",',"').replace('""','"').replace("',",'",').replace(",'",',"')
            obj = obj.replace('"}"}','"}').replace(':"',':').replace(':',':"')
            print(obj)
            all_contents[-1] = json.loads(obj)
            all_contents.append([])
safe_dump_to_json(data=all_contents,file_path='loggers.json')

input(safe_load_from_json(file_path='loggers.json'))








