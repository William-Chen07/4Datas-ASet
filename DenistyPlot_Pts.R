


RaceResults %>%
  ggplot(aes(x = Points, fill = TeamName)) +
  geom_density(alpha = .3)



