library(tidyverse)
library(rvest)
  
gen_tables <- function(year) {
  
  Sys.sleep(5)
  url <- glue::glue('https://www.pro-football-reference.com/years/{year}/fantasy.htm')
  data <- url %>%
    read_html() %>%
    html_table() %>%
    .[[1]]
  
  names(data) <- paste(names(data), data[1, ], sep = "_")
  data <- data[-1,]
  colnames(data)[1:5] <- c("RK", "Player", "Team", "FantPos", "Age")
  
  data <- data %>%
    filter(RK != 'Rk') %>%
    janitor::clean_names() %>%
    mutate_at(.vars = vars(age:fantasy_ov_rank), as.numeric) %>%
    mutate(year = year)
  return(data)
}


df <- tibble()
for (i in 2009:2019){
  print(i)
  scraped_table <- gen_tables(i)
  df <- rbind(df, scraped_table)
}

df <- df %>% 
  mutate(player = gsub('\\*', '',player))%>%
  mutate(player = gsub('\\+', '',player)) 

head(df)

