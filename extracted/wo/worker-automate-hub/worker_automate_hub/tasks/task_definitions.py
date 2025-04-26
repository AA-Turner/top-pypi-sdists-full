from worker_automate_hub.tasks.jobs.abertura_livros_fiscais import (
    abertura_livros_fiscais,
)
from worker_automate_hub.tasks.jobs.fidc_exportacao_docs_portal_b2b import (
    exportacao_docs_portal_b2b,
)
from worker_automate_hub.tasks.jobs.fidc_gerar_nosso_numero import gerar_nosso_numero
from worker_automate_hub.tasks.jobs.coleta_dje_process import coleta_dje_start_update
from worker_automate_hub.tasks.jobs.coleta_dje_process import (
    coleta_dje_start_update,
)
from worker_automate_hub.tasks.jobs.conexao_rdp import conexao_rdp
from worker_automate_hub.tasks.jobs.fechar_conexao_rdp import fechar_conexao_rdp
from worker_automate_hub.tasks.jobs.cte_manual import cte_manual
from worker_automate_hub.tasks.jobs.geracao_aprovacao_pedidos import (
    geracao_aprovacao_pedidos_171,
    geracao_aprovacao_pedidos_34,
)
from worker_automate_hub.tasks.jobs.notas_faturamento_sap import notas_faturamento_sap
from worker_automate_hub.tasks.jobs.descartes import descartes
from worker_automate_hub.tasks.jobs.ecac_estadual_main import (
    ecac_estadual_main,
)
from worker_automate_hub.tasks.jobs.ecac_federal import ecac_federal
from worker_automate_hub.tasks.jobs.entrada_de_notas_39 import entrada_de_notas_39
from worker_automate_hub.tasks.jobs.entrada_de_notas_207 import entrada_de_notas_207
from worker_automate_hub.tasks.jobs.entrada_de_notas_500 import entrada_de_notas_500
from worker_automate_hub.tasks.jobs.entrada_de_notas_9 import entrada_de_notas_9
from worker_automate_hub.tasks.jobs.entrada_de_notas_7139 import entrada_de_notas_7139
from worker_automate_hub.tasks.jobs.entrada_de_notas_36 import entrada_de_notas_36
from worker_automate_hub.tasks.jobs.entrada_de_notas_503 import entrada_de_notas_503
from worker_automate_hub.tasks.jobs.fidc_remessa_cobranca_cnab240 import (
    remessa_cobranca_cnab240,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_9 import (
    entrada_de_notas_9,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_15 import (
    entrada_de_notas_15,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_16 import (
    entrada_de_notas_16,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_32 import (
    entrada_de_notas_32,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_33 import (
    entrada_de_notas_33,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_34 import (
    entrada_de_notas_34,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_39 import (
    entrada_de_notas_39,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_207 import (
    entrada_de_notas_207,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_500 import (
    entrada_de_notas_500,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_505 import (
    entrada_de_notas_505,
)
from worker_automate_hub.tasks.jobs.entrada_de_notas_7139 import (
    entrada_de_notas_7139,
)
from worker_automate_hub.tasks.jobs.entrada_cte_333 import entrada_cte_333
from worker_automate_hub.tasks.jobs.entrada_cte_1353 import entrada_cte_1353
from worker_automate_hub.tasks.jobs.exemplo_processo import exemplo_processo
from worker_automate_hub.tasks.jobs.fidc_retorno_cobranca import retorno_cobranca
from worker_automate_hub.tasks.jobs.login_emsys import login_emsys
from worker_automate_hub.tasks.jobs.login_emsys_versao_especifica import (
    login_emsys_versao_especifica,
)
from worker_automate_hub.tasks.jobs.playground import playground
from worker_automate_hub.tasks.jobs.transferencias import transferencias
from worker_automate_hub.tasks.jobs.sped_fiscal import sped_fiscal
from worker_automate_hub.tasks.jobs.devolucao_prazo_a_faturar import (
    devolucao_prazo_a_faturar,
)
from worker_automate_hub.tasks.jobs.devolucao_ctf import devolucao_ctf
from worker_automate_hub.tasks.jobs.integracao_contabil import integracao_contabil

task_definitions = {
    "5b295021-8df7-40a1-a45e-fe7109ae3902": exemplo_processo,
    "a0788650-de48-454f-acbf-3537ead2d8ed": login_emsys,
    "7d319f61-5e12-425c-86ed-678f0d9e14bd": login_emsys_versao_especifica,
    "abcfa1ba-d580-465a-aefb-c15ac4514407": descartes,
    "2c8ee738-7447-4517-aee7-ce2c9d25cea9": transferencias,
    "855f9e0f-e972-4f52-bc1a-60d1fc244e79": conexao_rdp,
    "d36b0c83-9cc3-465f-ac80-934099a0e661": fechar_conexao_rdp,
    "457b8f50-4944-4107-8e1b-80cb9aedbd5d": notas_faturamento_sap,
    "81785803-0594-4bba-9aa0-7f220c200296": coleta_dje_start_update,
    "3907c8d4-d05b-4d92-b19a-2c4e934f1d78": ecac_estadual_main,
    "81d2d6e6-e9eb-414d-a939-d220476d2bab": ecac_federal,
    "bbab8ff5-3eff-4867-a4af-239273d896ee": entrada_de_notas_32,
    "9e5a1c05-9336-4b2d-814e-4d0e9f0057e1": entrada_de_notas_33,
    "08a112db-7683-417b-9a87-14ad0e1548da": entrada_de_notas_34,
    "1e354c95-f4e4-4e12-aaf6-4ef836cc741b": entrada_de_notas_36,
    "bf763394-918b-47be-bb36-7cddc81a8174": entrada_de_notas_39,
    "dafc0407-da8f-43a1-b97a-d27f966e122a": entrada_de_notas_207,
    "e1051c43-3495-4ca7-91d5-527fea2b5f79": entrada_de_notas_500,
    "f061c8f8-f862-410e-9de6-8bbc47b0ec74": entrada_de_notas_503,
    "d168e770-0c33-4e20-a7f9-977bf15542f3": entrada_de_notas_505,
    "8e61a6c6-aeb4-456d-9aa5-b83ab8be297d": entrada_de_notas_9,
    "1a53d689-3cfb-4ec0-a02c-b249224b12ac": entrada_de_notas_15,
    "811e8934-8227-4686-a030-df057c054f75": entrada_de_notas_16,
    "e19d48a4-850b-413e-81c3-808158711ea0": entrada_de_notas_7139,
    "a4154a69-a223-48c2-8ff6-535cd29ff2d4": playground,
    "8d45aa6b-e24c-464d-afba-9a3147b3f506": gerar_nosso_numero,  # Banco do Brasil FIDC
    "29338b70-4ae6-4560-8aef-5d0d7095a527": gerar_nosso_numero,  # Banco do Brasil S.A
    "0aa423c1-fc7f-4b7e-a2b2-a1012c09deae": remessa_cobranca_cnab240,
    "276d0c41-0b7c-4446-ae0b-dd5d782917cc": sped_fiscal,
    "5d8a529e-b323-453f-82a3-980184a16b52": devolucao_prazo_a_faturar,
    "19a8f0b4-f5bf-49e8-8bc2-4aeceeae95ec": retorno_cobranca,  # Retorno de cobrança
    "2db72062-4d11-4f91-b053-f4800f46c410": retorno_cobranca,  # Retorno de cobrança extraordinaria
    "abf3725f-d9d9-4f48-a31d-b22efb422e08": entrada_cte_333,
    "e9f9a463-c2b6-40cb-8d67-a80d0725b424": entrada_cte_1353,
    "cf25b3f3-b9f1-45b5-a8d2-8c087024afdc": devolucao_ctf,
    "f241dbd6-f4a7-4afb-822a-46a628cfc916": exportacao_docs_portal_b2b,  # FIDC
    "5ad2d209-e9da-438c-ba62-db0a5f9a3795": exportacao_docs_portal_b2b,  # Banco do brasil
    "326a746e-06ec-44c0-84bb-3a2dd866353e": cte_manual,
    "c7a53083-a364-45e2-a1f7-acd439fe8632": integracao_contabil,
    "e1696b6b-9de4-4f22-a977-b191a39506a9": integracao_contabil,
    "0745818a-4760-4cbe-b6bc-073519ac2104": integracao_contabil,
    "044a5713-82bd-4758-aec4-3a502d526568": integracao_contabil,
    "f76dae1d-799b-4b23-b83f-f688e6528f2c": integracao_contabil,
    "d94efc2a-8589-4fd3-b545-01a431ebe51f": integracao_contabil,
    "d94efc2a-8589-4fd3-b545-01a431ebe51f": integracao_contabil,
    "3bd9c06c-84c9-40d2-b76f-2eb3de391a99": integracao_contabil,
    "ebadbf8f-a381-4afd-bb8f-f3a2ed1aadf7": integracao_contabil,
    "7e8c3510-b2d7-4601-9a2d-4cd0d5888b2b": integracao_contabil,
    "7c1301a8-999a-4bd2-9d13-ee85df0a5e07": integracao_contabil,
    "664eb900-8a15-4752-a9a5-b4ca0c03f42f": integracao_contabil,
    "99cc717d-7629-479a-958e-b662ab12407b": integracao_contabil,
    "75b08d05-3623-40dc-a314-66ccbaea087c": integracao_contabil,
    "8b8c5b64-70f9-4bd4-9916-e807ba7b91d7": integracao_contabil,
    "bb1dc164-ea25-4acf-a10b-b7274078fdc0": integracao_contabil,
    "87c6b443-e9c4-4e93-bff8-b37de114b55d": integracao_contabil,
    "760f464d-b529-4a20-9ef5-7c3fdfb26cb8": integracao_contabil,
    "7da52552-ef26-4a43-aa2f-e15e96468fea": integracao_contabil,
    "e2e10bbf-8ff8-4bf1-8631-5ef35ea27c0c": integracao_contabil,
    "29bfeb03-35ac-41ac-a278-10b544de1372": integracao_contabil,
    "6cbf59c2-cea8-46b5-972e-dcaffdf714ed": integracao_contabil,
    "5434e3ef-7769-4864-a439-432ff48cb7da": integracao_contabil,
    "2d267df2-9851-45dd-bd5f-3552ae2f4c70": integracao_contabil,
    "02391b17-7fb6-4bbc-96fa-d80cbed1ad15": integracao_contabil,
    "cc924dc8-6f0c-475c-b034-2cfc1dd4cb34": integracao_contabil,
    "5134ff27-9cf1-4ffe-b923-7d273ccac88e": integracao_contabil,
    "fbf55a21-252a-4e17-9229-ea4d74308806": integracao_contabil,
    "afc4daf0-ab87-4370-bfce-04e10b6809c7": integracao_contabil,
    "aec31846-73a0-4879-bfa8-0d65ec0db28d": integracao_contabil,
    "d7d81211-778d-4d08-922c-428cfcb48b1f": integracao_contabil,
    "e7500e0f-084a-453f-8b3a-ddcf703e831e": integracao_contabil,
    "588e6baa-c90c-417d-ad7c-1c1e6251868a": integracao_contabil,
    "9ac39e07-6556-4fbe-ac66-b8ab31a2493d": integracao_contabil,
    "d071e48c-f1db-4291-846d-74a0dd345b57": integracao_contabil,
    "f128ea6f-d4ae-41d0-ab7c-7663510f988c": integracao_contabil,
    "2bec3c51-5794-4a46-8882-da8f6af8a39a": integracao_contabil,
    "6defc06b-b922-4124-b90d-2b053f5fdd3b": integracao_contabil,
    "8be6c166-a348-45bd-b0b0-6629b3da3c63": integracao_contabil,
    "bb28c2b1-1048-46f7-9a09-509f7205997b": integracao_contabil,
    "b72616f5-67d4-4734-a5d3-e6b3a598a510": integracao_contabil,
    "0ea3e899-aa3e-44ce-816b-62c217d8cf03": integracao_contabil,
    "3b92b7c1-8953-44c3-923a-d005e5d527f5": integracao_contabil,
    "c3aa2a8d-6577-4ca9-84b9-ab180de05037": integracao_contabil,
    "dc6b61b2-0147-450e-9da7-cae7eb699aec": integracao_contabil,
    "7072fe2a-de79-4b9e-8985-7be93c7e7ba9": integracao_contabil,
    "d60388f1-dc07-49d0-a154-ce318a529c1c": integracao_contabil,
    "30544b48-7dc4-4f3e-ac6c-16be7bca57a4": integracao_contabil,
    "c8527e90-c65b-4d68-b4cf-25008b678957": geracao_aprovacao_pedidos_34,
    "260380b7-a3e5-4c23-ab69-b428ee552830": geracao_aprovacao_pedidos_171,
    "c10bbf8c-3949-4a0e-9e10-3d85d367263d": abertura_livros_fiscais,
}


async def is_uuid_in_tasks(uuid_to_check):
    """
    Verifica se um UUID está presente nas definições de tarefas.

    :param uuid_to_check: O UUID a ser verificado.
    :return: True se o UUID estiver presente, False caso contrário.
    """
    return uuid_to_check in task_definitions.keys()
