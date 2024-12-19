/**
* Name: GAMAVisualize
* Based on the internal skeleton template. 
* Author: hnv
* Tags: 
*/

model GAMAVisualize

global {
	file Test_Path_file <- csv_file("../includes/path.csv",",");
	matrix Test_Path_matrix <- matrix(Test_Path_file);
	
	int num_robot_init <- 1;
	int num_of_goals <- 1;
	
	
	file Test_Grid_file  <- csv_file("../includes/grid_state.csv");
	matrix Test_Grid_matrix <- matrix(Test_Grid_file);
	
	int num_of_cols <- int(Test_Grid_matrix[0, 0]);
	int num_of_rows <- int(Test_Grid_matrix[0, 1]);
	
	int num_of_obstacle_in_each_iter <- 1;
	
	file Test_Goal_End <- csv_file("../includes/start_end.csv");
	matrix Test_Goal_End_Matrix <- matrix(Test_Goal_End);
	
	file Test_Path <- csv_file("../includes/path.csv");
	matrix Test_Path_Matrix <- matrix(Test_Path);
	int robot_step <- 0;
	
	init { 
		write(num_of_cols);
		write(num_of_rows);
		// Will be change due to randomize
		create goal number: num_of_goals {
			location <- point(Test_map_cell[int(Test_Goal_End_Matrix[0,1]),int(Test_Goal_End_Matrix[1,1])]);
		}
		create robot number: num_robot_init;
//		 {
//			location <- point(Test_map_cell[int(Test_Goal_End_Matrix[0,0]),int(Test_Goal_End_Matrix[1,0])]);
//		} 
		loop i from: 2 to: Test_Grid_matrix.rows -1 {
//			point include x, y, z but only use x, y
			point obstacle_pos <- point([float(Test_Grid_matrix[0, i]), float(Test_Grid_matrix[1, i])]);
			write(obstacle_pos);
			create obstacle number: num_of_obstacle_in_each_iter {
				location <- point(Test_map_cell[int(Test_Grid_matrix[1, i]), int(Test_Grid_matrix[0, i])]);
			}
		}
	}
}

species robot {
	//image_file my_icon <- image_file("../includes/robot.png");
	
	// Position variables for the robot
	float size <- 1.0;
	float x_pos <- 0.0;
	float y_pos <- 0.0;
	rgb color <- #blue;
	Test_map_cell robot_cell <- Test_map_cell[int(Test_Goal_End_Matrix[0,0]),int(Test_Goal_End_Matrix[1,0])]; 
	
	init {
		location <- robot_cell.location;
	}
	
	aspect base {
		draw circle(size) color: color;
	}
	
	reflex basic_move {
		robot_cell <- choose_cell();
		location <- robot_cell.location;
	}
	
	Test_map_cell choose_cell {
		Test_map_cell robot_next_cell <- Test_map_cell[int(Test_Path_Matrix[0, robot_step]),int(Test_Path_Matrix[1, robot_step])];
		robot_step <- robot_step + 1;
		return robot_next_cell;
	}
}

species goal {
	float size <- 1.0;
	aspect default { 
		draw circle(size) color: #red;
	}
}

species obstacle {
	float size <- 2.0;
	aspect default {
		draw rectangle(size, size) color: #black;
	}
} 

grid Test_map_cell width: num_of_cols height: num_of_rows neighbors: 4 {
	int is_obstacle <- 0;
//	rgb color <- is_obstacle ? #black : #white;
}

experiment GAMAVisualize type: gui {
	// Run the simulation to move the robot to each step
	parameter "Initial number of robot: " var: num_robot_init min: 1 max: 5 category: "Robot";
	output {
		display main_display {
			grid Test_map_cell border: #black;
			species robot aspect: base;
			species goal aspect: default ;
			species obstacle aspect: default;
		}
	}
}
