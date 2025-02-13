
ggplot(year_count, aes(x = Year, y = n)) +
  geom_col(fill = "steelblue") +
  labs(title = "Total Entries by Year",
       x = "Year",
       y = "Total Entries") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle=90)) +
  scale_x_continuous(breaks = seq(1800, 1960, by = 10))



