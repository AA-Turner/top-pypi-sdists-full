from . import *


@dataclass
class EmotionCore:
	intensity:float=0
	name:str=''
	dtoe:datetime=datetime.now()
	note:str=''

@dataclass
class EmotionCoreDB(BASE,Template):
	pass

