from adam.config import Config
from adam.utils_tabulize import tabulize
from adam.utils_context import Context

class NodeRestartable:
   def __init__(self, pod: str, downs: dict = None, dup_copies: set = None, host_ids_by_pod: dict[str, str] = [], err: str = None):
      self.pod = pod
      self.downs = downs
      self.dup_copies = dup_copies
      self.host_ids_by_pod = host_ids_by_pod
      self.err = err

   def restartable(self):
      if not Config().get('cassandra.restart.check-tokens-dup-hosting', True):
         return not self.downs

      return not self.downs and not self.dup_copies

   def log(self, ctx: Context = Context.NULL):
      if self.err:
          ctx.log2(f'[ERROR] {self.err}')

          return

      tabulize(sorted(list(self.host_ids_by_pod.keys())),
               lambda p: f'{p}\t{self.host_ids_by_pod[p]}',
               header='POD\tHOST_ID',
               separator='\t',
               ctx=ctx.copy(show_out=True, text_color=ctx.text_color))

      if self.downs:
            ctx.log2(f'[REPLICAS DOWN] The following nodes with replicas are down.')
            ctx.log2()

            downs = self.downs
            tabulize(sorted(list(downs.keys())),
                     lambda k: f'{downs[k]["status"]}\t{k}\t{downs[k]["pod"]}\t{downs[k]["namespace"]}\t{len(downs[k]["tokens"])}\t{downs[k]["in_restart"]}',
                     header='--\tAddress\tPOD\tNAMESPACE\t#_Tokens_Shared\tIn_Restart',
                     separator='\t',
                     text_color=ctx.text_color)

      if self.dup_copies:
            if self.downs:
               ctx.log2()
            ctx.log2(f'[MULTIPLE COPIES ON A SINGLE POD] {self.pod} hosts more than 1 repica of token ranges.')
            ctx.log2(f'  {", ".join(self.dup_copies)}')

      if not self.downs and not self.dup_copies:
            ctx.log2(f'{self.pod} can be restarted safely.')

   def waiting_on(self) -> str:
       if self.err:
         if 'is already in restart' in self.err:
            return self.err.split(' ')[0]

         return '-'

       if self.downs:
           ip = sorted(list(self.downs.keys()))[0]
           if 'pod' in self.downs[ip]:
               return f'DN: {self.downs[ip]["pod"]}'

           return '-'

       if self.dup_copies:
           return f'MC: {sorted(list(self.dup_copies))[0]}'

       return '-'