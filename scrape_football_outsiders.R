
library(tidyverse)
library(rvest)

gen_tables <- function(year) {
  
  Sys.sleep(5)
  url <- glue::glue('https://www.footballoutsiders.com/stats/nfl/pace-stats/{year}')
  data <- url %>%
    read_html() %>%
    html_table() %>%
    .[[1]] %>%
    janitor::clean_names() %>%
    mutate(season = year)
  return(data)
}


df <- tibble()
for (i in 2009:2019){
  print(i)
  scraped_table <- gen_tables(i)
  df <- rbind(df, scraped_table)
}

head(df)