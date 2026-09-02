from dotenv import load_dotenv
from openai import OpenAI
from matrx_utils import clear_terminal, vcprint

load_dotenv()
client = OpenAI()



def test_conversation_id():
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="tell me a joke",
    )
    print(response.output_text + "\n\n"+"="*50)

    second_response = client.responses.create(
        model="gpt-4o-mini",
        previous_response_id=response.id,
        input=[{"role": "user", "content": "explain why this is funny."}],
    )
    print("\n\n" + second_response.output_text)

    vcprint(second_response, "Second Response", color="green")


def retreive_by_id(id: str):
    response = client.responses.retrieve(id)
    vcprint(response, "Retrieved Response", color="green")

    
def test_with_hard_coded_id(id: str):
    response = client.responses.create(
        model="gpt-4.1-mini",
        previous_response_id=id,
        input=[{"role": "user", "content": "explain why this is funny."}],
    )
    print("\n\n" + response.output_text)
    vcprint(response, "Response", color="green")
    
if __name__ == "__main__":
    clear_terminal()
    hard_coded_id_1 = "resp_0bc087b1e8ad410a006956ae21f4ec8192ae9bdf9a58a3430c"
    hard_coded_id_2 = "resp_0bc087b1e8ad410a006956ae20b7e08192984494db03c98a42"
    
    # test_conversation_id()
    # test_with_hard_coded_id(hard_coded_id)
    retreive_by_id(hard_coded_id_1)
    retreive_by_id(hard_coded_id_2)