from configs import GainOrMaintainConfig

class DailyConsumption:
    """
    The task here is to:
    1. Obtain a config object based on gain or maintain
    2. Fetch and cache all food macros in JSON (to limit API calls)
    3. Generate combinations of foods to match config,
        using `calories` as a limit in a while loop
    4. Loop over all these combinations and select/save the ones
        that match the target macro ratios within a certain margin
        of error/epsilon.
    * We are creating a DAILY collection of foods since I may not
      eat the same number of meals each day, and since many smaller meals
      allow for higher calorie consumption.
    """
