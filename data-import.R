# This script is to install the necessary R packages, create a data directory, and read & write the NASCAR Cup Series driver career data to a CSV file. The file that is written will be loaded in Python to render the plot for the plotnine contest.

if (!require('readr')) install.packages('readr')

# setup to access data from nascaR.data package
if (!require('remotes')) install.packages('remotes')

# install nascaR.data package
remotes::install_github('kyleGrealis/nascaR.data')

# create data folder
if (!dir.exists(paste0(here::here(), "/data"))) {
  dir.create(paste0(here::here(), "/data"))
}

# load & save data
cup_race_data <- nascaR.data::cup_race_data
readr::write_csv(cup_race_data, 'data/cup_race_data.csv')
