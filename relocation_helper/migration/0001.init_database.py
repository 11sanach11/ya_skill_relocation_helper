# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
from yoyo import step

steps = [
    step("CREATE TABLE boxes (id INTEGER PRIMARY KEY, box_name TEXT NOT NULL);"),
    step("CREATE UNIQUE INDEX boxes_box_name on boxes (box_name);"),
    step("CREATE TABLE items (id INTEGER PRIMARY KEY, item_name TEXT NOT NULL, box_id INTEGER);"),
]
