import math
import torch
from torch import nn
from torch.nn import functional as F
from einops import rearrange



class BertEmbeddings(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.word_embeddings = nn.Embedding(config.vocab_size, config.hidden_size, padding_idx=config.pad_token_id)
        self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        self.register_buffer("position_ids", torch.arange(config.max_position_embeddings).expand((1, -1)))
        self.config = config

    def forward(self, input_ids, query_embeds):
        b, t = input_ids.shape
        position_ids = self.position_ids[:, :t]
        embeddings = self.word_embeddings(input_ids)
        position_embeddings = self.position_embeddings(position_ids)
        embeddings += position_embeddings
        embeddings = torch.cat((query_embeds, embeddings), dim=1)
        embeddings = self.LayerNorm(embeddings)
        return embeddings


class BertSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.num_attention_heads = config.num_attention_heads
        self.attention_head_size = config.hidden_size // config.num_attention_heads
        self.all_head_size = self.num_attention_heads * self.attention_head_size

        self.query = nn.Linear(config.hidden_size, self.all_head_size)
        self.key = nn.Linear(config.hidden_size, self.all_head_size)
        self.value = nn.Linear(config.hidden_size, self.all_head_size)

    def forward(
        self, 
        hidden_states,
        attention_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
    ):
        q, k, v = self.query(hidden_states), self.key(hidden_states), self.value(hidden_states)
        q, k, v = map(lambda x : rearrange(x, "B L (H D) -> B H L D", H=self.num_attention_heads), (q, k, v))
        # print("initial self hidden states", hidden_states.shape)
        # print(q.shape, k.shape, v.shape, attention_mask.shape)
        # print(attention_mask)
        attn = F.scaled_dot_product_attention(q, k, v, attention_mask)
        hidden_states = rearrange(attn, "B H L D -> B L (H D)")
        # print("final self hidden states", attn.shape)

        return hidden_states
    

class BertCrossAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.num_attention_heads = config.num_attention_heads
        self.attention_head_size = config.hidden_size // config.num_attention_heads
        self.all_head_size = self.num_attention_heads * self.attention_head_size

        self.query = nn.Linear(config.hidden_size, self.all_head_size)
        self.key = nn.Linear(config.encoder_width, self.all_head_size)
        self.value = nn.Linear(config.encoder_width, self.all_head_size)

    def forward(
        self, 
        hidden_states,
        attention_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
    ):
        # print("initial cross hidden states", hidden_states.shape)
        q, k, v = self.query(hidden_states), self.key(encoder_hidden_states), self.value(encoder_hidden_states)
        q, k, v = map(lambda t: rearrange(t, "B L (H D) -> B H L D", H=self.num_attention_heads), (q, k, v))

        attn = F.scaled_dot_product_attention(q, k, v, encoder_attention_mask)
        hidden_states = rearrange(attn, "B H L D -> B L (H D)")

        # print("final cross hidden states", hidden_states.shape)

        return hidden_states

class BertSelfOutput(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)

    def forward(self, hidden_states, input_tensor):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.LayerNorm(hidden_states + input_tensor)
        return hidden_states


class BertAttention(nn.Module):
    def __init__(self, config, cross=False):
        super().__init__()
        self.cross = cross
        self.self = BertCrossAttention(config) if cross else BertSelfAttention(config)
        self.output = BertSelfOutput(config)

    def forward(
        self,
        hidden_states,
        attention_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
    ):
        self_outputs = self.self(
            hidden_states,
            attention_mask,
            encoder_hidden_states,
            encoder_attention_mask,
        )
        attention_output = self.output(self_outputs, hidden_states)
        return attention_output


class BertIntermediate(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.intermediate_size)
        self.intermediate_act_fn = nn.GELU()

    def forward(self, hidden_states):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.intermediate_act_fn(hidden_states)
        return hidden_states


class BertOutput(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.intermediate_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)

    def forward(self, hidden_states, input_tensor):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.LayerNorm(hidden_states + input_tensor)
        return hidden_states


class BertCrossLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.attention = BertAttention(config)      
        self.crossattention = BertAttention(config, cross=True)
        self.intermediate = BertIntermediate(config)
        self.output = BertOutput(config)

        self.intermediate_query = BertIntermediate(config)
        self.output_query = BertOutput(config)

    def forward(
        self,
        hidden_states,
        attention_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
        query_length=None,
    ):
        attention_output = self.attention(hidden_states, attention_mask)
        query_attention_output = attention_output[:, :query_length, :]
        rest_attention_output = attention_output[:, query_length:, :]

        query_attention_output = self.crossattention(
            query_attention_output,
            attention_mask,
            encoder_hidden_states,
            encoder_attention_mask,
        )

        layer_output = self.output_query(self.intermediate_query(query_attention_output), query_attention_output)
        layer_output_text = self.output(self.intermediate(rest_attention_output), rest_attention_output)
        # print("layer output", layer_output.shape)
        # print("layer output text", layer_output_text.shape)
        layer_output = torch.cat([layer_output, layer_output_text], dim=1)
        # print("layer output", layer_output.shape)

        return layer_output


class BertLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.attention = BertAttention(config)
        self.intermediate = BertIntermediate(config)
        self.output = BertOutput(config)

        self.intermediate_query = BertIntermediate(config)
        self.output_query = BertOutput(config)

    def forward(
        self,
        hidden_states,
        attention_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
        query_length=None,
    ):
        attention_output = self.attention(hidden_states, attention_mask)
        query_attention_output = attention_output[:, :query_length, :]
        rest_attention_output = attention_output[:, query_length:, :]

        layer_output = self.output_query(self.intermediate_query(query_attention_output), query_attention_output)
        layer_output_text = self.output(self.intermediate(rest_attention_output), rest_attention_output)
        layer_output = torch.cat([layer_output, layer_output_text], dim=1)

        return layer_output



class BertEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.query_length = 32
        self.layer = nn.ModuleList([
            # alternate between BertLayer and BertCrossLayer
            BertCrossLayer(config) if i % 2 == 0 else BertLayer(config) for i in range(config.num_hidden_layers)
        ])

    def forward(
        self,
        hidden_states,
        attention_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
    ):               
        for i in range(self.config.num_hidden_layers):
            layer_module = self.layer[i]
            # print(f"pre layer {i} hidden states", hidden_states.shape)
            hidden_states = layer_module( hidden_states, attention_mask, encoder_hidden_states, encoder_attention_mask, query_length=self.query_length)
            # print(f"post layer {i} hidden states", hidden_states.shape)

        return hidden_states


class BertModel(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.embeddings = BertEmbeddings(config)
        self.encoder = BertEncoder(config)
     
    def forward(
        self,
        input_ids=None,
        query_embeds=None,
        attention_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
    ):
        extended_attention_mask = attention_mask[:, None, None, :].to(torch.bool)
        encoder_extended_attention_mask = encoder_attention_mask[:, None, None, :].to(torch.bool)
        embedding_output = self.embeddings(input_ids=input_ids, query_embeds=query_embeds)
            
        encoder_outputs = self.encoder(
            embedding_output,
            attention_mask=extended_attention_mask,
            encoder_hidden_states=encoder_hidden_states,
            encoder_attention_mask=encoder_extended_attention_mask,
        )

        return encoder_outputs


class BertPredictionHeadTransform(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.transform_act_fn = nn.GELU(approximate="tanh")
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)

    def forward(self, hidden_states):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.transform_act_fn(hidden_states)
        hidden_states = self.LayerNorm(hidden_states)
        return hidden_states

class BertLMPredictionHead(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.transform = BertPredictionHeadTransform(config)

        self.decoder = nn.Linear(config.hidden_size, config.vocab_size, bias=False)

        self.bias = nn.Parameter(torch.zeros(config.vocab_size))

        self.decoder.bias = self.bias

    def forward(self, hidden_states):
        hidden_states = self.transform(hidden_states)
        hidden_states = self.decoder(hidden_states)
        return hidden_states

class BertOnlyMLMHead(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.predictions = BertLMPredictionHead(config)

    def forward(self, sequence_output):
        prediction_scores = self.predictions(sequence_output)
        return prediction_scores


class BertLMHeadModel(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.bert = BertModel(config)
        self.cls = BertOnlyMLMHead(config)

    def forward(self, input_ids, attention_mask=None, encoder_hidden_states=None, encoder_attention_mask=None):
        outputs = self.bert(input_ids, attention_mask, encoder_hidden_states, encoder_attention_mask)
        prediction_scores = self.cls(outputs)
        return prediction_scores