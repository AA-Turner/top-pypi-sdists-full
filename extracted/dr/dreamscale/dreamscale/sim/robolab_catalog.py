"""RoboLab's tasks and suites for `dreamscale sim robolab --list` (offline).

RoboLab-120 at commit ad45d4f, the class names a hosted run accepts as ``--task-id``. The hosted
service validates every run against its own copy of this list.
"""

from __future__ import annotations

ROBOLAB_TASKS: tuple[str, ...] = (
    "AnimalsInBinTask", "AppleAndYogurtInBowlTask", "BBQSauceInBinTask", "BagelsOnPlateTask",
    "BananaInBowlTask", "BananaOnPlateTask", "BananaThenRubiksCubeTask",
    "BananasInBinOneMoreTask", "BananasInBinThreeTotalTask", "BananasInCrateTask",
    "BananasOutOfBinTask", "BigPumpkinInBinTask", "BlackItemsInBinTask",
    "BlockStackingOrderAgnosticTask", "BlockStackingSpecifiedOrderTask", "BlocksInBinTask",
    "BowlInBinTask", "BowlStackingLeftOnRightTask", "BowlStackingRightOnLeftTask",
    "ButterAboveRaisinTask", "CannedFoodInBinTask", "ClampInRightBinTask", "CleanUpToysTask",
    "ClearOrganicObjectsTask", "ClutterPlasticTask", "ClutterPumpkinTask",
    "CoffeePotInBinTask", "CondimentsInBinTask", "CookingClearPlateTask",
    "CookingPickPastaToolTask", "CubesAndBlocksInBinTask", "DishesInBinTask",
    "ElectronicsInBinTask", "FoodPacking1BoxesTask", "FoodPacking1CansTask",
    "FoodPacking2BoxesTask", "FoodPacking2CansTask", "FoodPacking3BoxesTask",
    "FoodPacking3CansTask", "FoodPackingByColorTask", "FruitsGreenLimesOnPlateTask",
    "FruitsMovingOrangeOrLimeTask", "FruitsMovingTask", "FruitsOnPlate3Task",
    "FruitsOnPlateTask", "FruitsOnionTask", "FruitsOnionToPlateTask",
    "FruitsOrangesOnPlateTask", "GrabABagelTask", "GrabAFruitTask", "GreenSpoonsInPotTask",
    "HammersInLeftBinTask", "JugsOnShelfTask", "KeyboardOutOfBinTask",
    "LargerObjectRaisinBoxInBinTask", "MarkerInMugTask", "MouseOnKeyboardTask",
    "MoveBananaToBagelPlateTask", "MustardAboveRaisinTask", "MustardInLeftBinTask",
    "MustardInRightBinTask", "NonHammerToolsInRightBinTask", "OneBottleInSquarePailTask",
    "OneBottleOnShelfTask", "PhoneOrRemoteInBinTask", "PickDrillTask", "PickGlassesTask",
    "PickOrangeObjectTask", "PickUpBluePitcherTask", "PickUpGreenObjectTask",
    "PinkSpoonInPotTask", "PlasticBottlesInSquarePailTask", "PutBowlOnShelfTopTask",
    "PutMugsOnShelfTask", "PutTwoMugsOnShelfTask", "RecycleCartonTask",
    "RecycleCartonsOnBoxTask", "RecycleCartonsVerticalCrateTask", "RedDishesInBinTask",
    "RedItemsInBinTask", "ReorientAllMugsTask", "ReorientJugTask", "ReorientRedMugTask",
    "ReorientWhiteMugsTask", "RubiksCubeAndBananaTask", "RubiksCubeBehindBowlTask",
    "RubiksCubeInFrontOfBowlTask", "RubiksCubeLeftOfBowlTask", "RubiksCubeOrBananaTask",
    "RubiksCubeRightOfBowlTask", "RubiksCubeTask", "RubiksCubeThenBananaTask",
    "RubiksCubesInBinTask", "SauceBottlesCrateTask", "SmallPumpkinInBinTask",
    "SmallerObjectButterInBinTask", "SmartphoneInBinTask", "SpoonInMugTask", "SpoonsInPotTask",
    "Stack3RubiksCubeTask", "StackWhiteMugsTask", "StackYellowOnRedTask",
    "TakeMeasuringSpoonOutTask", "TakeMugsOffOfShelfTask", "TakeSpatulaOffShelfTask",
    "ThrowAwayAppleTask", "ThrowAwaySnacksTask", "ToolOrganizationBothTask",
    "ToolOrganizationTask", "ToolsPickingAllHammersTask", "ToolsPickingDrillTask",
    "ToolsPickingHammerTask", "ToyInBinTask", "UnstackRubiksCubeTask", "UtensilsInMugTask",
    "WhiteMugInCenterOfTableTask", "WhiteMugsInBinTask", "WoodSpatulaToBowlTask",
    "YellowAndWhiteObjectsInBinTask", "YogurtInBowlTask",
)

# smoke10: ten single-object tasks across bowls, mugs, plates, bins and tools.
SUITES: dict[str, tuple[str, ...]] = {
    "smoke10": (
        "BananaInBowlTask", "RubiksCubeTask", "MarkerInMugTask", "SpoonInMugTask",
        "YogurtInBowlTask", "BagelsOnPlateTask", "PickDrillTask", "ToyInBinTask",
        "MouseOnKeyboardTask", "WhiteMugInCenterOfTableTask",
    ),
    "all": ROBOLAB_TASKS,
}
