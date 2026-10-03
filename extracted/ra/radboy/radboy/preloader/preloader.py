from . import *
from radboy.SystemSettings.SystemSettings import *

preloader={
	f'{uuid1()}':{
						'cmds':['roll the die','flip a coin','rtd','fac'],
						'desc':f'flip a coin, or roll the die, to determine order of presedence',
						'exec':rollTheDie,
					},
	f'{uuid1()}':{
						'cmds':['volume',],
						'desc':f'find the volume of height*width*length without dimensions',
						'exec':volume
					},
	f'{uuid1()}':{
						'cmds':['depreciation','price out','fire sale'],
						'desc':f'calculate info for firesale',
						'exec':depreciation,
					},
	f'{uuid1()}':{
            'cmds':['glossary','g'],
            'exec':lambda:GlossaryUI(engine=ENGINE),
            'desc':'terms and definitions related to inventory management'
            	},
    f'{uuid1()}':{
            'cmds':['algebraic','alg'],
            'exec':algrebaic_calculator,
            'desc':'an algebraic prepped form of ce'
            	},
    f'{uuid1()}':{
            'cmds':['discount','dscnt'],
            'exec':discount,
            'desc':'calculate discount price details'
            	},
    f'{uuid1()}':{
            'cmds':['max discount','mdscnt'],
            'exec':max_discount_allowed,
            'desc':'calculate maximum allowed discount price details'
            	},
    f'{uuid1()}':{
            'cmds':['annual percentage yield','apy'],
            'exec':annual_percentage_yield,
            'desc':'annual percentage yield'
            	},
    f'{uuid1()}':{
            'cmds':['percent change','prcnt chng'],
            'exec':percent_change,
            'desc':'percent change = ((new-old)/old)*100'
            	},
    f'{uuid1()}':{
            'cmds':['rate of change','rt of chng'],
            'exec':rate_of_change,
            'desc':'rate of change = (new-old)/across'
            	},
	f'{uuid1()}':{
			'cmds':['dpr4rwi','daily periodic rate to find real world interest'],
			'exec':daily_periodic_rate_to_find_real_world_interest,
			'desc':'daily periodic rate to find real world interest'
				},
    f'{uuid1()}':{
			'cmds':['average daily balance','adb'],
			'exec':averageDailyBalance,
			'desc':'sum month end of day balances and divide by the sum of the days in that month for averageDailyBalance'
				},       	
    f'{uuid1()}':{
            'cmds':['compound interest standard','cis'],
            'exec':compound_interest_standard,
            'desc':'compound_interest_standard formula = principle*((1+(r/n))**(n*t)) = total amount'
            	},
    f'{uuid1()}':{
		    'cmds':['compound interest contributing','cic'],
		    'exec':compound_interest_contributing,
		    'desc':'compound_interest_standard formula = principle*((1+(r/n))**(n*t)) + ((((1+(r/n))**(n*t))-1)/(r/n))*payment'
    			},    	
    f'{uuid1()}':{
            'cmds':['lawn job','ljb'],
            'exec':lawnjobLogger,
            'desc':'record details about a lawn job'
            	},
    f'{uuid1()}':{
            'cmds':['transaction id','tid'],
            'exec':transactionIDLogger,
            'desc':'manage transaction ids'
            	},
    f'{uuid1()}':{
            'cmds':['gift card maxes','gcm'],
            'exec':giftCardMaxesLogger,
            'desc':'set gift card maxes for a retailer'
            	},
    f'{uuid1()}':{
            'cmds':['cashier quizlet','cashq'],
            'exec':CashierQuizlet,
            'desc':'Cashier Quizlet Giving Change'
            	},
    f'{uuid1()}':{
            'cmds':['cashier quizlet no auto','cashqna'],
            'exec':CashierQuizletAuto,
            'desc':'Cashier Quizlet Giving Change no auto grade no prompt'
            	},
    f'{uuid1()}':{
            'cmds':['qp',"question pool","?p","?pool","qpool"],
            'exec':questionPoolLogger,
            'desc':'create new questions from python scripts for use with "cashqna"'
            	},
    f'{uuid1()}':{
            'cmds':['bt',"break time",],
            'exec':Break_Time,
            'desc':"Get The Time for your break; keep track of your breaks"
            	},
    f'{uuid1()}':{
            'cmds':['qty=(dist*trips)/mpg',"qdtm",],
            'exec':QTY_eq_distanceXtrip_over_mpg,
            'desc':"(QTY=Distance*Trips)/MPG[economy]"
            	},
    f'{uuid1()}':{
            'cmds':['mt',"meal time",],
            'exec':Meal_Time,
            'desc':'"Get The Time for your Meal; keep track of your Meals"'
            	},
    f'{uuid1()}':{
            'cmds':['cfc','change from cash'],
            'exec':change_from_cash,
            'desc':'Calculate Change to Give Customer From (Price - Cash Given)'
            	},
    f'{uuid1()}':{
            'cmds':['find zip code','fzc'],
            'exec':find_zip_code,
            'desc':'find a zip code'
            	},
    f'{uuid1()}':{
            'cmds':['calorie intake','ci','calin'],
            'exec':calorieIntakeLogger,
            'desc':'record your calorie intake'
            	},
    f'{uuid1()}':{
            'cmds':['basic food log','bfl','basic-food-log'],
            'exec':basicFoodLogLogger,
            'desc':'record basic food taken'
            	},
    f'{uuid1()}':{
            'cmds':['name from entry search','nfes','name from name barcode code','nfnbc'],
            'exec':nameFromSearch,
            'desc':'get and return EntryName from Search of Barcode,Name,Code'
            	},
    f'{uuid1()}':{
            'cmds':['iefc','import entry from child'],
            'exec':get_from_child_db,
            'desc':'import a Entry row from a db in the boot directory'
            	},
    f'{uuid1()}':{
            'cmds':['atndnc','attendance','abstnt','absent','is present','isprsnt','is prsnt'],
            'exec':AttendanceLogger,
            'desc':'keep track of employee attendance'
            	},
    f'{uuid1()}':{
            'cmds':['rdzne frt','rzf','rztd','red zone truck day',],
            'exec':RedZoneFreightLogger,
            'desc':'red zone freight that is not counted towards truck'
            	},
    f'{uuid1()}':{
            'cmds':['till drawer loadout','tll dwr ldt','tdl'],
            'exec':tilldrawerloadoutLogger,
            'desc':'preload a till for practice counting back'
            	},
    f'{uuid1()}':{
            'cmds':['cooling estimates','clest'],
            'exec':coolingLogger,
            'desc':'generate a cooling estimate for your dwelling'
            	},
    f'{uuid1()}':{
            'cmds':['custom unit registry','cur'],
            'exec':customUnitLogger,
            'desc':'Add Custom Units that get loaded when booting and when printing to variable `ureg`'
            	},
    f'{uuid1()}':{
            'cmds':['wtfday','wtfd','wtf'],
            'exec':wtfdayLogger,
            'desc':'log a bad day, what the ****!'
            	},
    f'{uuid1()}':{
            'cmds':['schedule','skdl','schdl'],
            'exec':scheduleLogger,
            'desc':'log a schedule something'
            	},
    f'{uuid1()}':{
            'cmds':['cvt','convert from to'],
            'exec':Convert,
            'desc':'convert a value from one unit to another'
            	},
    f'{uuid1()}':{
            'cmds':['transport trip name','ttn','a2z','a-to-z'],
            'exec':transport_trip_name,
            'desc':'generate a transport trip name for casecounting'
            	},
    f'{uuid1()}':{
            'cmds':['iiw','i interacted with','iInteractedWith','i-interacted-with'],
            'exec': i_InteractedWithLogger,
            'desc':'log whom i interacted with during the day to keep myself safe'
            	},
    f'{uuid1()}':{
            'cmds':['fdlbl','fd lbl','food label','food-label'],
            'exec': foodlabelLogger,
            'desc':'log food label info'
            	},
    f'{uuid1()}':{
            'cmds':['storage paths','sp'],
            'exec':storagePathsLogger,
            'desc':'add storage paths for side loading data from other dbs; to enable the path for use with iefc, ensure group_id contains "active"'
            	},
    f'{uuid1()}':{
            'cmds':['offset clock','oc'],
            'exec':offsetClockLogger,
            'desc':'view the different clock times around the house by offset'
            	},
    f'{uuid1()}':{
            'cmds':['emolog','emo log','emotion log','eml'],
            'exec':emotionLogger,
            'desc':'log an emotion'
            	},
    f'{uuid1()}':{
            'cmds':['foa','fuel over area','fuel useage mower','fum'],
            'exec':FuelOverArea,
            'desc':'get your fuel efficiency for your lawn mower'
            	},
    f'{uuid1()}':{
            'cmds':['format entry insert script','feis'],
            'exec':FormatEntryInsertScript,
            'desc':'generate a entry format script on loop to paste with pyperclip if supperted'
            	},
    f'{uuid1()}':{
            'cmds':['required materials list','rml'],
            'exec':requiredMaterialsLogger,
            'desc':'required materials list before being used in mksl/qsl list maker'
            	},
    f'{uuid1()}':{
            'cmds':['accronym from name','afn'],
            'exec':Accronym,
            'desc':'generate an accronym from name'
            	},
    f'{uuid1()}':{
            'cmds':['nen','new entry name'],
            'exec':NewEntryName,
            'desc':'generate a new entry name from gathered details'
            	},
    f'{uuid1()}':{
            'cmds':['ooty','hour of the year','hour_of_the_year','hour-of-the-year','hour/of/the/year','hour.of.the.year'],
            'exec':HourOfTheYear,
            'desc':'take an input date and determine what day,hour,minute,second of the year it correlates to'
            	},
    f'{uuid1()}':{
            'cmds':['clock to decimal','c2d','clock 2 decimal','clock2decimal','clock-decimal','clk2dec'],
            'exec':ClockToDecimal,
            'desc':'convert time (base24(hour)/base60(min)/base60(sec)) to decimal format (base10) 2:30==2.5 && 22:30==22.5'
            	},
	f'{uuid1()}':{
						'cmds':['qty str','qts','qty s',],
						'desc':f'generate a qty text for use with Entry.Note',
						'exec':QtyString
					},
	f'{uuid1()}':{
						'cmds':['dsr','door seal registry',],
						'desc':f'log/register door seals for use with door seals',
						'exec':DoorSealRegistryLogger
					},
	f'{uuid1()}':{
						'cmds':['dsl','door seal log',],
						'desc':f'log door seals in use with door secured doors',
						'exec':DoorSealLogLogger
					},
	f'{uuid1()}':{
						'cmds':['bmtc','bare min to cmplt'],
						'desc':f'bare minimum to compete =totalToComplete/DaysToComplete',
						'exec':BareMinimumToComplete
					},
	f'{uuid1()}':{
						'cmds':['hww','height weight waist'],
						'desc':f'track you body\'s size, weight, and height',
						'exec':HeightWeightWaistLogger
					},
	f'{uuid1()}':{
						'cmds':['pcl','piece count logger'],
						'desc':f'track you store load counts',
						'exec':PieceCountLogger
					},
	f'{uuid1()}':{
						'cmds':['sibdsd','shipping invoice by department sub department'],
						'desc':f'shipping invoice by department sub department',
						'exec':ShippingInvoice_By_Dept_SubDeptLogger
					},
	f'{uuid1()}':{
						'cmds':['dcdpl','dc dlvry prp lggr'],
						'desc':f'DC Delivery Preparation Logger',
						'exec':DC_Delivery_PreparationLogger
					},
	f'{uuid1()}':{
						'cmds':['asui','aprv str use','approved store use logger'],
						'desc':f'ApprovedStoreUseLogger for items that are for store use',
						'exec':ApprovedStoreUseLogger
					},
	f'{uuid1()}':{
						'cmds':['mdae','mk dwn & xprds','markdown and expireds'],
						'desc':f'MarkDownsAndExpireds for items that are about to expire or need to be marked down. ',
						'exec':MarkDownsAndExpiredsLogger
					},
	f'{uuid1()}':{
						'cmds':['rndm prc','random price'],
						'desc':f'generate a random price float within 0 to 75; for tills',
						'exec':RandomPrice
					},
	f'{uuid1()}':{
						'cmds':['rndm chng','random change'],
						'desc':f'generate a random change from price float - customer payment within 0 to 75; for tills',
						'exec':RandomChange
					},
	f'{uuid1()}':{
						'cmds':['chkio','check in out'],
						'desc':f'generate a check in check out string from subsequent data provided by the user',
						'exec':CheckInOut
					},
	'{uuid1()}':{
						'cmds':['sp vlm','secific volume'],
						'desc':f'calculate volume/mass=specificVolume',
						'exec':SpecificVolume
					},
	f'{uuid1()}':{
						'cmds':['lwpl','local weather pattern logger'],
						'desc':f'record local weather data for preview in a later context',
						'exec':LocalWeatherPatternLogger
					},
	f'{uuid1()}':{
						'cmds':['cstmr pay','customer pays what'],
						'desc':f'generate a random payment float that is within 0 to 75+0-10% random extra ; for tills',
						'exec':RandomCustomerPayment
					},
	f'{uuid1()}':{
						'cmds':['dtc','days to cmplt',],
						'desc':f'Days To Complete = totalToComplete/BareMinimumToComplete',
						'exec':DaysToComplete
					},
	f'{uuid1()}':{
						'cmds':['ttc','ttl to cmplt',],
						'desc':f'Total To Complete = BareMinimumToComplete*DaysToComplete',
						'exec':TotalToComplete
					},
	f'{uuid1()}':{
						'cmds':['oil log','oillog','oil'],
						'desc':f'log oil filled into engine',
						'exec':oillogLogger,
					},
	f'{uuid1()}':{
						'cmds':['aumup','unmark all as unpaid/do not log',],
						'desc':f'un-mark all in list as unpaid/do not log',
						'exec':All_UnMarkUnPaid
					},
	f'{uuid1()}':{
						'cmds':['cost report','cr',],
						'desc':f'cost report',
						'exec':CostReport
					},
	f'{uuid1()}':{
		'cmds':['lse',],
		'desc':f'display the current list',
		'exec':ListBuild
	},
	f'{uuid1()}':{
						'cmds':['amup','mark all unpaid',],
						'desc':f'mark all in list as unpaid/do not log',
						'exec':All_MarkUnPaid
					},
	f'{uuid1()}':{
						'cmds':['ae2l','add eid 2 list',],
						'desc':f'add entryid to list',
						'exec':addLstQtyById
					},
	f'{uuid1()}':{
						'cmds':['bdystts','body stats','bdsts'],
						'desc':f'track blood pressure and body temperature',
						'exec':bodyStatsLogger,
					},
	f'{uuid1()}':{
						'cmds':['prsrv','per serving',],
						'desc':f'how much is served using serving size, served, and amount per serving',
						'exec':per_serving,
					},
	f'{uuid1()}':{
						'cmds':['fcl','feed consumption logger','feed consumption log'],
						'desc':f'animal/pet feed log',
						'exec':fclLogger,
					},
	f'{uuid1()}':{
						'cmds':['employer info','employer info logger','eil'],
						'desc':f'record employer info',
						'exec':employer_infoLogger,
					},
	f'{uuid1()}':{
						'cmds':['daily budget','dly bdgt',],
						'desc':f'calculate your daily budget',
						'exec':daily_budget,
					},
	f'{uuid1()}':{
						'cmds':['billing text','bilt',],
						'desc':f'generate billing text for listmaking',
						'exec':billing_text_gen,
					},
	f'{uuid1()}':{
						'cmds':['count per mil','cpm','qty for width','qfw','qty for length','qfl','count for length','count for width','cfl','cfw'],
						'desc':f'get total units for units per 1 of unit',
						'exec':count_per_mil,
					},
	f'{uuid1()}':{
						'cmds':['csbh','change shift by hours',],
						'desc':f'change shift by hours',
						'exec':moveShift,
					},
	f'{uuid1()}':{
						'cmds':['bank transfer text','btt',],
						'desc':f'generate bank transfer text for listmaking',
						'exec':bank_transfer_text,
					},
	f'{uuid1()}':{
						'cmds':['bill paid text','bpt','bptxt','bp text'],
						'desc':f'generate bill paid text for listmaking',
						'exec':bill_paid_text,
					},
	f'{uuid1()}':{
						'cmds':['ttw','tried to wake',],
						'desc':f'TRIED TO WAKE LOGGER',
						'exec':ttwLogger,
				},
	f'{uuid1()}':{
						'cmds':['dmur','dmu rvw','date metrics update review'],
						'desc':f'review datemetrics data',
						'exec':dmuLogger,
				},
	f'{uuid1()}':{
						'cmds':['sl','symptom logger','slog','symlog',],
						'desc':f'make a symptom log',
						'exec':symptomLogger,
				},
	f'{uuid1()}':{
			'cmds':['sysset','system settings menu','ssm','system settings'],
			'desc':f'System Settings Menu',
			'exec':systemSettingsMenu,
	},
	f'{uuid1()}':{
						'cmds':['tpoc','tasks pending or complete',],
						'desc':f'chores list',
						'exec':tpocLogger,
				},
	f'{uuid1()}':{
						'cmds':['crspdnc','correspondence','messages','msgs','txtmsg','txt msg','accusation','acstn','accused','acsd'],
						'desc':f'When someone sends me a message and I am feeling like there may be some danger use this list, or if i feel like i am being accused of something',
						'exec':CorrespondenceLogger,
				},
	f'{uuid1()}':{
						'cmds':['hmnwst','human waste','hmn wst','gut health','gth'],
						'desc':f'record your human waste details to get an idea of your health',
						'exec':HumanWasteLogger,
				},
	f'{uuid1()}':{
						'cmds':['rstrm','breaks','restroom','brks',],
						'desc':f'record breaks and restroom breaks that are excessive for plotting details to prove restroom/breaks are being abused',
						'exec':RestroomBreakLogger,
				},
	f'{uuid1()}':{
						'cmds':['frt strt end','fse','freight start end',],
						'desc':f'record the starting and ending freight given to personnel for the day; to be used with FreightEnd to see how much was done before being used in a freight cleared log.',
						'exec':FreightStartEndLogger,
				},
	f'{uuid1()}':{
						'cmds':['fzn strt end','fzse','frozen start end',],
						'desc':f'record the starting and ending frozen given to personnel for the day; to be used with FrozenStartEnd to see how much was done before being used in a freight cleared log.',
						'exec':FrozenStartEndLogger,
				},
	f'{uuid1()}':{
						'cmds':['fzn rxd','fzn rcvd','frozen recieved','frozen rcvd','ftruck day','ftd'],
						'desc':f'record the record the load size from the truck recieved on dtoe',
						'exec':FrozenRecievedLogger,
				},
	f'{uuid1()}':{
						'cmds':['br strt end','brse','backroom start end',],
						'desc':f'record the starting and ending frozen given to personnel for the day; to be used with FrozenStartEnd to see how much was done before being used in a freight cleared log.',
						'exec':BackroomStartEndLogger,
				},
	f'{uuid1()}':{
						'cmds':['br rxd','br rcvd','backroom recieved','backroom rcvd','brtruck day','brtd'],
						'desc':f'record the record the load size from the truck recieved on dtoe',
						'exec':BackroomRecievedLogger,
				},
	f'{uuid1()}':{
						'cmds':['fbr strt end','fbrse','frozen backroom start end',],
						'desc':f'record the starting and ending frozen given to personnel for the day; to be used with FrozenStartEnd to see how much was done before being used in a freight cleared log.',
						'exec':FrozenBackroomStartEndLogger,
				},
	f'{uuid1()}':{
						'cmds':['fbr rxd','fbr rcvd','frozen backroom recieved','frozen backroom rcvd','fbrtruck day','fbrtd'],
						'desc':f'record the record the load size from the truck recieved on dtoe',
						'exec':FrozenBackroomRecievedLogger,
				},
	f'{uuid1()}':{
						'cmds':['ssnl strt end','ssnlse','seasonal start end',],
						'desc':f'record the starting and ending seasonal given to personnel for the day; to be used with FrozenStartEnd to see how much was done before being used in a freight cleared log.',
						'exec':SeasonalStartEndLogger,
				},
	f'{uuid1()}':{
						'cmds':['ssnl rxd','ssnl rcvd','seasonal backroom recieved','seasonal backroom rcvd','seasonal truck day','ssnltd'],
						'desc':f'record the record the load size from the truck recieved on dtoe',
						'exec':SeasonalRecievedLogger,
				},
	f'{uuid1()}':{
						'cmds':['npl','notepod logger','ntpd'],
						'desc':f'record a note or instructions that can be grouped',
						'exec':notePodLogger,
				},
	f'{uuid1()}':{
					'cmds':['ogl','oil grade logger',],
					'desc':f'record a oil grade used in a macine for future reference',
					'exec':oilGradeLogger,
			},
	f'{uuid1()}':{
				'cmds':['vhcl reg','vehicle registration',],
				'desc':f'record a vehicle registration cards data',
				'exec':vehicleRegistrationLogger,
		},
		f'{uuid1()}':{
				'cmds':['drvr lcns','drivers license',],
				'desc':f'record drivers license data',
				'exec':driversLicenseLogger,
		},
		f'{uuid1()}':{
				'cmds':['id card','state id card',],
				'desc':f'record state id card data',
				'exec':stateIdCardLogger,
		},
		f'{uuid1()}':{
						'cmds':['random dtoe','rnd dtoe','rdtoe'],
						'desc':f'generate a random dtoe',
						'exec':lambda: randomDate(start_year=Control(ptext='Start Year',helpText="smallest year",data="integer"),end_year=Control(ptext='End Year',helpText="largest year",data="integer")),
				},
	f'{uuid1()}':{
						'cmds':['dry br strt end','dbrse','dairy backroom start end',],
						'desc':f'record the starting and ending frozen given to personnel for the day; to be used with FrozenStartEnd to see how much was done before being used in a freight cleared log.',
						'exec':DairyBackroomStartEndLogger,
				},
	f'{uuid1()}':{
						'cmds':['dry br rxd','dry br rcvd','dairy backroom recieved','dairy backroom rcvd','dbrtruck day','dbrtd'],
						'desc':f'record the record the load size from the truck recieved on dtoe',
						'exec':DairyBackroomRecievedLogger,
				},
	f'{uuid1()}':{
						'cmds':['dry strt end','dse','dairy start end',],
						'desc':f'record the starting and ending frozen given to personnel for the day; to be used with FrozenStartEnd to see how much was done before being used in a freight cleared log.',
						'exec':DairyStartEndLogger,
				},
	f'{uuid1()}':{
						'cmds':['ds','dstring','date string',],
						'desc':f'return a date string in mm/dd/yyyy',
						'exec':DateString1,
				},
	f'{uuid1()}':{
						'cmds':['ds+','dstring+','date string from dtoe',],
						'desc':f'return a date string in mm/dd/yyyy from dtoe',
						'exec':DateString2,
				},
	f'{uuid1()}':{
						'cmds':['dry rxd','dry rcvd','dairy recieved','dairy rcvd','dtruck day','dtd'],
						'desc':f'record the record the load size from the truck recieved on dtoe',
						'exec':DairyRecievedLogger,
				},
	f'{uuid1()}':{
						'cmds':['pwr otg','no power', 'npwr','power is out','power outage'],
						'desc':f'record the record power outage',
						'exec':PowerOutageLogger,
				},
	f'{uuid1()}':{
						'cmds':['frt rxd','frt rcvd','freight recieved','freight rcvd','truck day','td'],
						'desc':f'record the record the load size from the truck recieved on dtoe',
						'exec':FreightRecievedLogger,
				},
	f'{uuid1()}':{
						'cmds':['bills','blls','rent','electric','utilities','water',],
						'desc':f'log and keep track of your bills',
						'exec':BillsLogger,
				},
	f'{uuid1()}':{
						'cmds':['tpoc2','tasks completed',],
						'desc':f'tasks that i need to do at street address, geolocation, start dtoe, end dtoe, compensated for what, with name_Desc',
						'exec':tpoc2Logger,
				},
	f'{uuid1()}':{
						'cmds':['ddsl','dewey decimal system logger',],
						'desc':f'log, search dewey decimal system numbers',
						'exec':deweyDecimalSystemLogger,
				},
	f'{uuid1()}':{
						'cmds':['date metrics update','dmu',],
						'desc':f'update date metrics manually',
						'exec':lambda: print(f"Weather Collection is done:{theNASWeather()}"),
				},
	f'{uuid1()}':{
						'cmds':['date metrics update async','dmua',],
						'desc':f'update date metrics manually using async',
						'exec':lambda: print(f"Weather Collection is done:{asyncio.run(theWeather())}"),
	},
	f'{uuid1()}':{
						'cmds':['gc','garbage collection',],
						'desc':f'gc module tools, garbage collection',
						'exec':GarbageCollection,
	},
	f'{uuid1()}':{
						'cmds':['gas2','gas logger 2',],
						'desc':f'extended gas logger ; plan your trips and the cost of gas accordingly',
						'exec':gas2Logger,
				},
	f'{uuid1()}':{
						'cmds':['inradius','ir','r=A/s',],
						'desc':f'inradius=area / semi_perimeter',
						'exec':inRadius_Area_over_SemiPerimeter,
				},
	f'{uuid1()}':{
						'cmds':['inradius a+b-c/2','ir a+b-c/2','r=(a+b-c)/2',],
						'desc':f'inradius=(side a + side b - side c)/2',
						'exec':inRadius_a_plus_b_minus_2_over2,
				},
	f'{uuid1()}':{
						'cmds':['inradius sqrt((s-side a)*(s-side b)*(s-side c))/s','ir herons','ir heron',],
						'desc':f'inradius=sqrt((s-side a)*(s-side b)*(s-side c))/s ; herons formula',
						'exec':inRadius_herons,
				},
	f'{uuid1()}':{
						'cmds':['lwpl2','local weather pattern logger 2',],
						'desc':f'local weather logger extended',
						'exec':lwpl2Logger,
				},
	f'{uuid1()}':{
						'cmds':['recreational','prescribed','rx','meds','medications'],
						'desc':f'track your medications',
						'exec':medicationsLogger,
					},
	f'{uuid1()}':{
						'cmds':['rented rental','rnt rntl'],
						'desc':f'log your rental information',
						'exec':rented_rentalLogger,
					},
	f'{uuid1()}':{
						'cmds':['closeout','clst','cls t'],
						'desc':f'ensure a register is counted correctly',
						'exec':closeOutLogger,
					},
	f'{uuid1()}':{
						'cmds':['deposit','dpst',],
						'desc':f'count the deposit by weight',
						'exec':depositLogger,
					},
	f'{uuid1()}':{
						'cmds':['safe','sf',],
						'desc':f'count the safe by weight',
						'exec':safeLogger,
					},
	f'{uuid1()}':{
						'cmds':['extxt','expense text','xpnstxt','xpns txt'],
						'desc':f'generate expense text',
						'exec':ExpenseText,
					},
	f'{uuid1()}':{
						'cmds':['federal tax withholding',],
						'desc':f'calculate your tax withholding for federal; you will need the IRS Publication 15-T ({datetime.now().year})',
						'exec':FederalIncomeTaxWithholding
					},
	f'{uuid1()}':{
						'cmds':['va state tax withholding',],
						'desc':f'calculate your tax withholding for va state; you will need the "Virginia/VA Employer Withholding Tables" for ({datetime.now().year})',
						'exec':VAStateIncomeTaxWithholding
					},
	f'{uuid1()}':{
						'cmds':['mpgl','mpg log','mpg logger','miles per gallon log'],
						'desc':f'log your miles per gallon, make sure you have a start odometer reading, end odometer reading, and fuel used.',
						'exec':lambda: str(MPGLogger())
					},
	f'{uuid1()}':{
						'cmds':['fpl','fuel price log','fuel log','gas prices','gas'],
						'desc':f'log gas prices for trip planning',
						'exec':lambda: str(GasLogger())
					},
	f'{uuid1()}':{
						'cmds':['value from total mass','vftm'],
						'desc':f'give an estimated total value for mass of currency ((1/unitMass)*ValueOfUnit)*TotalMassOfUnitToBeCounted',
						'exec':TotalCurrencyFromMass
					},
	f'{uuid1()}':{
						'cmds':['base value from mass','bvfm'],
						'desc':f'get base value for each coin to use as the price so qty may be the gram value (1/unitMass)*ValueOfUnit',
						'exec':BaseCurrencyValueFromMass
					},
	f'{uuid1()}':{
						'cmds':['us currency mass','us cnc'],
						'desc':f'get us currency mass values',
						'exec':USCurrencyMassValues
					},
	f'{uuid1()}':{
						'cmds':['drgs','drugs','drug-select','drug select'],
						'desc':f'return a selected drug text',
						'exec':drug_text
					},
	f'{uuid1()}':{
						'cmds':['temp logger','temp log','tmplg'],
						'desc':f'log a temperature',
						'exec':lambda: str(Templogger())
					},
	f'{uuid1()}':{
						'cmds':['temp logger 2','temp log 2','tmplg2'],
						'desc':f'log a temperature',
						'exec':lambda: str(tmplg2Logger())
					},
	f'{uuid1()}':{
						'cmds':['mulefraud','mule fraud','mule-fraud','tax fraud mulisha','tax fraud 11.8.2025','consumer fraud 11.8.2025'],
						'desc':f'see what tax fraud values might look like',
						'exec':TaxMuleFraud
					},
	f'{uuid1()}':{
						'cmds':['volume pint',],
						'desc':f'find the volume of height*width*length using pint to normalize the values',
						'exec':volume_pint
					},
	f'{uuid1()}':{
						'cmds':['cooking units','cvt unts','cooking conversion','ck cvt'],
						'desc':f'review conversions for the kitchen; cooking conversions',
						'exec':CC_Ui
					},
	f'{uuid1()}':{
						'cmds':['self-inductance pint',],
						'desc':f'find self-inductance using pint to normalize the values for self-inductance=relative_permeability*(((turns**2)*area)/length)*1.26e-6',
						'exec':inductance_pint
					},
	f'{uuid1()}':{
						'cmds':['required resonant LC inductance',],
						'desc':f'find the resonant inductance for LC using L = 1 / (4π²f²C)',
						'exec':resonant_inductance
					},
	f'{uuid1()}':{
						'cmds':['cost to run','c2r'],
						'desc':f'find the cost to run a device per day',
						'exec':costToRun
				    },
	f'{uuid1()}':{
						'cmds':['now to % time','n2pt','trip planner','time to go','time to cross distance'],
						'desc':f'now to percent time, or time to go, so you can plan your trips and how much time you will need before even getting started',
						'exec':ndtp
				    },
	f'{uuid1()}':{
						'cmds':['currency conversion','cur-cvt'],
						'desc':f'convert currency from one to the another',
						'exec':currency_conversion,
				    },
	f'{uuid1()}':{
						'cmds':['sonofman-bible','sonofman','bible','bbl'],
						'desc':f'open sonofman bible',
						'exec':bible_try,
				    },
	f'{uuid1()}':{
						'cmds':['sales floor location','sls flr lctn'],
						'desc':f'generate a sales floor location string',
						'exec':SalesFloorLocationString,
				    },
	f'{uuid1()}':{
						'cmds':['backroom location','br lctn'],
						'desc':f'generate a backroom location string',
						'exec':BackroomLocation,
				    },
	f'{uuid1()}':{
						'cmds':['generic item or service text template','txt gios '],
						'desc':f'find the cost to run a device per day',
						'exec':generic_service_or_item
				    },
	f'{uuid1()}':{
						'cmds':['reciept book entry','rbe'],
						'desc':f'reciept book data to name template',
						'exec':reciept_book_entry,
				    },
	f'{uuid1()}':{
						'cmds':['air coil',],
						'desc':f''' 
The formula for inductance - using toilet rolls, PVC pipe etc. can be well approximated by:

                (0.394) * (r**2) * (N**2)
Inductance L = _________________________
              	( 9 * r ) + ( 10 * Len)
Here:
	N = Number of Turns 
	r = radius of the coil i.e. form diameter (in cm.) divided by 2
	Len = length of the coil - again in cm.
	L = inductance in uH.
	* = multiply by
	math.pi**2==0.394
						''',
						'exec':air_coil
					},
					f'{uuid1()}':{
						'cmds':['circumference of a circle using diameter',],
						'desc':f'C=2πr',
						'exec':circumference_diameter
					},
					f'{uuid1()}':{
						'cmds':['circumference of a circle using radius',],
						'desc':f'C=2πr',
						'exec':circumference_radius
					},
					f'{uuid1()}':{
						'cmds':['area of a circle using diameter',],
						'desc':f'A = πr²',
						'exec':area_of_circle_diameter
					},
					f'{uuid1()}':{
						'cmds':['area of a circle using radius',],
						'desc':f'A = πr²',
						'exec':area_of_circle_radius
					},
					f'{uuid1()}':{
						'cmds':['get capacitance for desired frequency with specific inductance',],
						'desc':f'C = 1 / (4π²f²L)²',
						'exec':air_coil_cap,
					},
					f'{uuid1()}':{
						'cmds':['get resonant frequency for lc circuit',],
						'desc':f'f = 1 / (2π√(LC))',
						'exec':lc_frequency,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['area','a'])],
						'desc':f'A=BH/2 = area of a triangle',
						'exec':area_triangle,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['ohms law','ohms-law','ohmslaw','ol'],endCmd=['resistance','resist','ohms','ohm','r','o'])],
						'desc':f'find resistance in ohms from Voltage(Volts)/Amperage(Current)',
						'exec':ohms_law_resistance,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['ohms law','ohms-law','ohmslaw','ol'],endCmd=['current','crnt','amps','amp','a'])],
						'desc':f'find current in ohms from Voltage(Volts)/Resistance(Ohm)',
						'exec':ohms_law_current,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['ohms law','ohms-law','ohmslaw','ol'],endCmd=['voltage','volts','vlt','v'])],
						'desc':f'find current in ohms from Amperage(Current)*Resistance(Ohm)',
						'exec':ohms_law_voltage,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['power dissipation','pwr dsptn','pwr dpn',],endCmd=['wattage','watts','watt','w','pwr','power'])],
						'desc':f'find Watts from Amperage(Current)*Voltage(Volts)',
						'exec':power_dissipation_watt,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['power dissipation','pwr dsptn','pwr dpn',],endCmd=['(i**2)*r','i_sqr_r','i2r',])],
						'desc':f'find Watts from (Amperage(Current)**2)*Resistance(Ohm)',
						'exec':power_i2_times_r,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['power dissipation','pwr dsptn','pwr dpn',],endCmd=['(v**2)/r','v_sqr_over_r','v**2/r',])],
						'desc':f'find Watts from (Voltage(Volts)**2)/Resistance(Ohm)',
						'exec':power_v2_over_r,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['amp','ampere',],endCmd=['(p/r)**0.5',])],
						'desc':f'find amperes from square_root(power/resistance)',
						'exec':amp_sqrt_power_over_r,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['volt','volts',],endCmd=['(p*r)**0.5',])],
						'desc':f'find volts from (P*R)**0.5',
						'exec':volt_sqrt_power_mult_resistance,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['ohm','ohms',],endCmd=['p/(i**2)',])],
						'desc':f'find ohms from power/(current**2)',
						'exec':ohm_power_over_i_squared,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['ohm','ohms',],endCmd=['(v**2)/p',])],
						'desc':f'find ohms from (voltage**2)/power',
						'exec':ohm_v_squared_over_p,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['reactance','rctnc',],endCmd=['inductive','2PifL','L'])],
						'desc':f'find inductive reactance from (2PifL)',
						'exec':inductive_reactance,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['reactance','rctnc',],endCmd=['capacitive','1/(2PifC)','C'])],
						'desc':f'find capacitive reactance is 1/(2PifC).',
						'exec':capacitive_reactance,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['power dissipation','pwr dsptn','pwr dpn',],endCmd=['voltage','volts','vlt','v'])],
						'desc':f'find Voltage(Volts) by Power(Watts)/Current(Amp)',
						'exec':power_dissipation_volt,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['power dissipation','pwr dsptn','pwr dpn',],endCmd=['current','crnt','amps','amp','a'])],
						'desc':f'find Amperage(Ampere||Amp) by Power(Watts)/Voltage(Volts)',
						'exec':power_dissipation_amp,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['impedance','mpdnc'],endCmd=['resistor capacitor inductor','rlc'])],
						'desc':f'find impedance of rlc = sqr root((r**2)+((xl-xc)**2)',
						'exec':impedance_rlc,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['impedance','mpdnc'],endCmd=['resistor capacitor','rc'])],
						'desc':f'find impedance of rc = sqr root((r**2)+(xc**2))',
						'exec':impedance_rc,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['impedance','mpdnc'],endCmd=['resistor inductor','rl'])],
						'desc':f'find impedance of rlc = sqr root((r**2)+(xl**2))',
						'exec':impedance_rl,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['job','jb'],endCmd=['applied to','at'])],
						'desc':f'record jobs aplied to',
						'exec':jobAppliedToLogger,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['ned','new entry data'],endCmd=['',' '])],
						'desc':f'generate a new entry data string for name',
						'exec':generate_item_name_sku,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['voltage','volt'],endCmd=['1p/dc drop',])],
						'desc':f'find voltage drop using (2LIR)/1000 for single-phase AC or DC circuits',
						'exec':single_phase_DC_voltage_drop,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['voltage','volt'],endCmd=['3p drop',])],
						'desc':f'find voltage drop using ((3**0.5)*LIR)/1000 for three(3p)-phase AC',
						'exec':three_phase_voltage_drop,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['cross sectional area','csa',],endCmd=['',' '])],
						'desc':f'find cross_sectional_area_meters using radius',
						'exec':cross_sectional_area_meters,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['resistance','ohm',],endCmd=['resistivity','ohm-meter','rstvty'])],
						'desc':f'find resistance in ohms using rho*(length/cross_sectional_area_meters)',
						'exec':resistance_csa_rstvty_lng,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['resistance','ohm',],endCmd=['tcorf','temperature coefficient of resistivity formula'])],
						'desc':f'find how electrical resistivity changes linearly with temperature for most metals over a normal range of temperatures. the linear temperature dependence of resistivity formula (or simply the temperature coefficient of resistivity formula).',
						'exec':temperature_coefficient_of_resistivity,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['resistance','ohm',],endCmd=['tcorf w/tdiff','temperature coefficient of resistivity formula just temp diff'])],
						'desc':f'find how electrical resistivity changes linearly with temperature for most metals over a normal range of temperatures. the linear temperature dependence of resistivity formula (or simply the temperature coefficient of resistivity formula). temperature change is already calculated.',
						'exec':temperature_coefficient_of_resistivity_pre_temp_diff,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['capacitance','farad','cap'],endCmd=['coulomb / volt','q/v'])],
						'desc':f'find capacitance_farad = charge_coulomb / volts_volt',
						'exec':capacitance_charge_voltage,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['total energy dissipated over time','tedot'],endCmd=['power_watt / time_seconds','pw*ts'])],
						'desc':f'find total energy dissipated over time = power_watt / time_seconds',
						'exec':total_energy_dissipated_over_time,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['hypotenus','hyp','hy'])],
						'desc':f'hypotenus of tiangle with height and base',
						'exec':solvefor_triangle_hypotenuse,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['base','bs'])],
						'desc':f'base of triangle with hypotenuse and height',
						'exec':solvefor_triangle_base,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['height','ht'])],
						'desc':f'height of triangle with hypotenuse and base',
						'exec':solvefor_triangle_height,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['soh','sine opposite hypotenuse','hy'])],
						'desc':f'[SOH]find Adj=sin(angle)*Opp the side opposite the angle (SOH CAH TOA) | Opposite and Hypotenuse [find length] needs Opposite side sin',
						'exec':soh_side_opposite_angle,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['cah','cosine adjacent hypotenuse'])],
						'desc':f'[CAH]find Opp=cos(angle)*hypotenuse the side adjacent the angle (SOH CAH TOA) | Adjacent and Hypotenuse [find length] needs Adjacent side cos',
						'exec':cah_side_adjacent_angle,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['toa','tangent opposite adjacent'])],
						'desc':f'[TOA]find Opp=tan(angle)*Adj or Adj=tan(angle)*Opp (SOH CAH TOA) | Opposite and Adjacent [find length] needs Hypotenuse side tan',
						'exec':toa_side_oppOrAdj_when_you_have_opposite_or_adjacent,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['asoh','arc sine opposite hypotenuse','hy'])],
						'desc':f"[aSOH]find math.degrees(math.asin(fb['opposite of Angle to find']/fb['hypotenuse'])) arc(SOH CAH TOA) | Opposite and Hypotenuse [find angle] needs Opposite angle asin",
						'exec':asoh_side_opposite_angle,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['acah','arc cosine adjacent hypotenuse'])],
						'desc':f"[aCAH]find math.degrees(math.acos(fb['adjacent of Angle to find']/fb['hypotenuse'])) arc(SOH CAH TOA) | Adjacent and Hypotenuse [find angle] needs Adjacent angle acos",
						'exec':acah_side_adjacent_angle,
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['triangle','trngl'],endCmd=['atoa','arc tangent opposite adjacent'])],
						'desc':f"[aTOA]find math.degrees(math.acos(fb['side opposite of Angle to find']/fb['side adjacent of Angle to find'])) arc(SOH CAH TOA) | Opposite and Adjacent [find angle] atan",
						'exec':atoa_side_oppOrAdj_when_you_have_opposite_or_adjacent,
					},
					f'{uuid1()}':{
						'cmds':['taxable kombucha',],
						'desc':f'is kombucha taxable?[taxable=True,non-taxable=False]',
						'exec':lambda: Taxable.kombucha(None),
					},
					f'{uuid1()}':{
						'cmds':['taxable item',],
						'desc':f'is item taxable?[taxable=True,non-taxable=False]',
						'exec':lambda: Taxable.general_taxable(None),
					},
					f'{uuid1()}':{
						'cmds':['price * rate = tax',],
						'desc':f'multiply a price times its tax rate ; {Fore.orange_red_1}Add this value to the price for the {Fore.light_steel_blue}Total{Style.reset}',
						'exec':lambda: price_by_tax(total=False),
					},
					f'{uuid1()}':{
						'cmds':['( price + crv ) * rate = tax',],
						'desc':f'multiply a (price+crv) times its tax rate ; {Fore.orange_red_1}Add this value to the price for the {Fore.light_steel_blue}Total{Style.reset}',
						'exec':lambda: price_plus_crv_by_tax(total=False),
					},
					f'{uuid1()}':{
						'cmds':['(price * rate) + price = total',],
						'desc':f'multiply a price times its tax rate + price return the total',
						'exec':lambda: price_by_tax(total=True),
					},
					f'{uuid1()}':{
						'cmds':['( price + crv ) + (( price + crv ) * rate) = total',],
						'desc':f'multiply a (price+crv) times its tax rate plus (price+crv) and return the total',
						'exec':lambda: price_plus_crv_by_tax(total=True),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['cylinder','clndr'],endCmd=['vol rad','volume radius'])],
						'desc':f'obtain the volume of a cylinder using radius',
						'exec':lambda: volumeCylinderRadius(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['cylinder','clndr'],endCmd=['vol diam','volume diameter'])],
						'desc':f'obtain the volume of a cylinder using diameter',
						'exec':lambda: volumeCylinderDiameter(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['cone',],endCmd=['vol rad','volume radius'])],
						'desc':f'obtain the volume of a cone using radius, a cone is 1/3 of a cylinder at the same height and radius',
						'exec':lambda: volumeConeRadius(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['cone',],endCmd=['vol diam','volume diameter'])],
						'desc':f'obtain the volume of a cone using diameter, a code is 1/3 of a cylinder at the same height and diameter',
						'exec':lambda: volumeConeDiameter(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['hemisphr','hemisphere'],endCmd=['vol rad','volume radius'])],
						'desc':f'obtain the volume of a hemisphere using radius',
						'exec':lambda: volumeHemisphereRadius(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['hemisphr','hemisphere'],endCmd=['vol diam','volume diameter'])],
						'desc':f'obtain the volume of a hemisphere using diameter',
						'exec':lambda: volumeHemisphereDiameter(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['circle',],endCmd=['area radius','area rad'])],
						'desc':f'obtain the area of a circle using radius',
						'exec':lambda: areaCircleRadius(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['circle',],endCmd=['area diameter','area diam'])],
						'desc':f'obtain the area of a circle using diameter',
						'exec':lambda: areaCircleDiameter(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['sudoku',],endCmd=['candidates','cd'])],
						'desc':f'obtain candidates for sudoku cell',
						'exec':lambda: sudokuCandidates(),
					},
					f'{uuid1()}':{
						'cmds':[i for i in generate_cmds(startcmd=['sudoku',],endCmd=['candidates auto','cda'])],
						'desc':f'obtain candidates for sudoku cell for the whole grid',
						'exec':lambda: candidates(),
					},
					f'{uuid1()}':{
						'cmds':['herons formula','hrns fmla'],
						'desc':f'''
Heron's formula calculates the area of any 
triangle given only the lengths of its 
three sides (a, b, and c). The formula is: 
Area = √(s(s-a)(s-b)(s-c)). To use it, first
 calculate the semi-perimeter, s = (a + b 
 + c) / 2, and then substitute this value 
 and the side lengths into the formula to 
 find the area. 
						''',
						'exec':lambda: heronsFormula(),
					},
					f'{uuid1()}':{
						'cmds':['tax add','atx'],
						'desc':'''AddNewTaxRate() -> None

add a new taxrate to db.''',
						'exec':lambda: AddNewTaxRate(),
					},
					f'{uuid1()}':{
						'cmds':['tax get','gtx'],
						'desc':	'''GetTaxRate() -> TaxRate:Decimal

search for and return a Decimal/decc
taxrate for use by prompt.
''',
						'exec':lambda: GetTaxRate(),
					},
					f'{uuid1()}':{
						'cmds':['tax delete','dtx'],
						'desc':'''DeleteTaxRate() -> None

search for and delete selected
taxrate.
''',
						'exec':lambda: DeleteTaxRate(),
					},
					f'{uuid1()}':{
						'cmds':['tax edit','etx'],
						'desc':'''EditTaxRate() -> None

search for and edit selected
taxrate.
''',
						'exec':lambda: EditTaxRate(),
					},
}
