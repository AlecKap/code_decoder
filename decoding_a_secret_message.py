import requests
from bs4 import BeautifulSoup
import re

def display_secret_code(doc):
  rows = convert_response_to_table_rows(doc)
  list_of_coords_and_symbol(rows)
  grid = build_grid(rows)[0]
  max_y_axis = build_grid(rows)[2]
  populate_grid(rows, grid, max_y_axis)
  display_grid(grid)

# helper methods

def convert_response_to_table_rows(doc):
  response = requests.get(doc)
  soup = BeautifulSoup(response.content, 'html.parser')
  table = soup.find('table')
  rows = table.find_all('tr')
  return rows

def list_of_coords_and_symbol(rows):
  coords_and_symbol = []
  for row in rows[1:]:
    groups_of_coords = re.match(r'(\d+)(\W)(\d+)', row.text)
    x,y = int(groups_of_coords[1]), int(groups_of_coords[3])
    symbol = groups_of_coords[2]
    if symbol:
      coords_and_symbol.append((x, y, symbol))
  return coords_and_symbol

def build_grid(rows):
  max_x_axis = max(x for x, y, symbol in list_of_coords_and_symbol(rows))
  max_y_axis = max(y for x, y, symbol in list_of_coords_and_symbol(rows))

  grid = [[' ' for _ in range(max_x_axis + 1)] for _ in range(max_y_axis + 1)]
  return [grid, max_x_axis, max_y_axis]

def populate_grid(rows, grid, max_y_axis):
  for x, y, symbol in list_of_coords_and_symbol(rows):
    grid[max_y_axis - y][x] = symbol

def display_grid(grid):
  for row in grid:
    print(''.join(row))



# display_secret_code('https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub')
display_secret_code('https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub')
