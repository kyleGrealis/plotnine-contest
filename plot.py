# %%
from plotnine import *
import polars as pl

# %%
drivers = (
    pl.read_csv('data/driver_data.csv')
    .sort(pl.col('career_wins'), descending=True)
    .head(n=5)
    .with_columns(
        pl.col('driver')
        .cast(pl.Categorical, categories=drivers['driver'].unique())
    )
)

driver_colors = {
    'Richard Petty': '#04aeec',
    'David Pearson': '#630727',
    'Jeff Gordon':  '#fc3812',
    'Bobby Allison': '#e4be8f',
    'Darrell Waltrip': '#24987a'
}

# %%
(
    ggplot(drivers)
    + geom_bar(
        aes(x='reorder(driver, career_wins)', y='career_wins', fill='driver'), 
        stat='identity', color='black', alpha=0.7
    )
    + geom_text(
        aes(x='driver', y='career_wins', label='career_wins'), 
        nudge_y=-8, color='black'
    )
    + coord_flip()
    + theme_classic()
    + scale_fill_manual(values=driver_colors)
    + labs(
        title='NASCAR Cup Series Top Winning Drivers',
        subtitle='Career wins',
        caption='Source: NASCAR.com (July 9, 2024)',
        x='', 
        y='Career Wins'
    )
    + theme(
        legend_position='none',
        plot_title=element_text(color='black', face='bold'),
        plot_subtitle=element_text(color='gray'),
        plot_caption=element_text(color='gray'),
        axis_text=element_text(color='black')
    )
)
