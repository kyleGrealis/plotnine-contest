# %%
import pandas as pd
from plotnine import *
from siuba import (_, arrange, case_when, count, filter, group_by, inner_join,
    mutate, ungroup, summarize)


import_df = (
    pd.read_csv('data/cup_race_data.csv', low_memory=False)
    >> filter(_.season == 2024)
)

counts = (
    import_df
    >> group_by(_.driver)
    >> count()
    >> filter(_.n >= 10)
    >> ungroup()
)

season_finish = (
    import_df
    >> inner_join(_, counts, by = 'driver')
    >> group_by(_.driver)
    >> summarize(avg_finish = _.finish.mean().round(2))
)

last_5_finish = (
    import_df
    >> inner_join(_, counts, by = 'driver')
    >> filter(_.race >= 16)
    >> group_by(_.driver)
    >> summarize(last_5_races = _.finish.mean().round(2))
)

# %%
race = (
    inner_join(season_finish, last_5_finish, by = 'driver')
    >> arrange(_.avg_finish)
    >> mutate(
        change = case_when({
            _.last_5_races < _.avg_finish: 'green',
            _.last_5_races == _.avg_finish: 'gray',
            _.last_5_races > _.avg_finish: 'red'
        }),
        # avg_finish = _.avg_finish * -1
    )
)

# %%
(
    race
    >> ggplot()
    + geom_bar(
        aes(x='reorder(driver, -avg_finish)', y='avg_finish * -1', fill='change'), 
        stat='identity', color='black', alpha=0.7
    )
    + geom_bar(
        aes(x='reorder(driver, -avg_finish)', y='last_5_races', fill='change'), 
        stat='identity', color='black', alpha=0.7
    )
    + geom_text(
        aes(x='driver', y=-28, label='round(avg_finish, 1)'), 
        nudge_y=-3, color='black', size=7
    )
    + annotate(
        'text', x=37, y=-28, label='Season', size=7,
        ha='right', va='top'
    )
    + geom_text(
        aes(x='driver', y=28, label='round(last_5_races, 1)'), 
        nudge_y=3, color='black', size=7
    )
    + annotate(
        'text', x=37, y=28, label='Last 5 Races', size=7,
        ha='center', va='top'
    )
    + coord_flip()
    + labs(
        title='NASCAR Cup Series 2024 Driver\'s Average Finish',
        subtitle='A comparison of season average finish versus average \nfinishing position over the last five races (through Chicago \nStreet Course on Sunday July 7, 2024)',
        caption='Source: NASCAR.com\nRendered by: Kyle Grealis',
        x='', y=''
    )
    + scale_fill_manual(values=['green', 'red'])
    + theme_classic()
    + theme(
        legend_position='none',
        plot_title=element_text(color='black', face='bold'),
        plot_subtitle=element_text(color='gray', face='bold'),
        plot_caption=element_text(color='gray'),
        axis_text=element_text(color='black'),
        axis_text_x=element_blank(),
    )
)
