library(tidyverse) # Data Cleaning, manipulation, summarization, plotting
library(ggthemes) # custom pre-built themes
library(teamcolors) # NFL team colors and logos
library(ggimage)

nfl_logos_df <- read_csv("https://raw.githubusercontent.com/statsbylopez/BlogPosts/master/nfl_teamlogos.csv")


df %>%
  filter(team == 'Avg') %>%
  select(season, sec_play_situation_neutral) %>%
  rename(avg_situation = sec_play_situation_neutral) %>%
  left_join(df, ., by=c('season')) %>%
  left_join(team_logos, by=c('team')) %>%
  left_join(team_colors, by=c('team')) %>%
  mutate(pace =avg_situation - sec_play_situation_neutral) %>%
  filter(season > 2018, team!= 'Avg')%>%
  ggplot(aes(x=reorder(team,pace),y=pace)) +
  geom_col(aes(fill=color), alpha=.8, width = .7) +
  geom_image(aes(image=team_logo)) +
  coord_flip() +
  scale_fill_identity(aesthetics = c('fill', 'colur')) +
  theme_fivethirtyeight() +
  theme(
    panel.grid.major.y = element_blank(),
    axis.text.y = element_blank(),
    axis.title.y = element_blank(),
    legend.position = 'none',
    plot.title = element_text(hjust=0.5)
  ) +
  geom_hline(yintercept = 0) +
  scale_y_continuous(breaks = seq(-3, 3, .5))+
  labs(
    title = 'Pace in Neutral Game Script Compared to League Average',
    caption= 'Data: FB Outsiders | Chart: @RyanPlain'
  )
ggsave('FILENAME.png', dpi=1000)
