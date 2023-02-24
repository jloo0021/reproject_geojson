#!/usr/bin/env Rscript Ctrl+shift+C

#libraries
#.libPaths(c("/Library/Frameworks/R.framework/Versions/4.1/Resources/library", .libPaths()))
suppressPackageStartupMessages(library(optparse))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(sf))
# suppressPackageStartupMessages(library(tidyr))
suppressPackageStartupMessages(library(RPostgreSQL))
# suppressPackageStartupMessages(library(data.table))

# option_list = list(
#   make_option(c("-f", "--file"), type="character", default=NULL, 
#               help="dataset file name", metavar="character"),
#   make_option(c("-o", "--out"), type="character", default="out.txt", 
#               help="output file name [default= %default]", metavar="character")
# ); 

# extract the database name that was passed in from the command line
option_list = list(
  make_option(c("-d", "--database"), type="character", default=NULL, 
              help="database name", metavar="character"),
  make_option(c("-s", "--database_schema"), type="character", default=NULL, 
              help="schema database name, where indicators are stored", metavar="character"),
  make_option(c("-o", "--output_location"), type="character", default=NULL, 
              help="output file location name", metavar="character")
); 
opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

# extracting the options passed in from the command line
DB_NAME<-opt$database
DB_NAME_SCHEMA<-opt$database_schema
output_location<-opt$output_location

# cat(paste0("Attempting calculateWomble.R with the following parameters:\n"))
# cat(paste0("database:        ",DB_NAME,"\n"))
# cat(paste0("database_schema: ",DB_NAME_SCHEMA,"\n"))
# cat(paste0("output_location: ",output_location,"\n\n"))

DB_NAME='wombleSA12011';
DB_NAME_SCHEMA='test_schema';

# # connect to the database
# conn = dbConnect(PostgreSQL(), dbname=DB_NAME, user="postgres", password="", host="localhost")
# conn_schema = dbConnect(PostgreSQL(), dbname=DB_NAME_SCHEMA, user="postgres", password="", host="localhost")
# 
# # all of the partitions that make up the city region
# indicators <- dbGetQuery(
#   conn_schema,
#   "SELECT sa1, dwelling, person, r_uli AS urban_liveability_index,
#    r_si_mix AS social_infrastructure_mix, r_walk_22 AS walkability,
#    r_hous_03 AS local_employment, r_os_public_14 AS closest_pos,
#    r_food_26 AS closest_healthy_food FROM observatory.sa1_melbourne_2018_v;"
# )

indicators <- read.csv("C:/Users/Joshua/OneDrive/Documents/Multiviz Internship/R Code/liveability_sa1_2011.csv")
boundaries <- st_read("C:/Users/Joshua/OneDrive/Documents/Multiviz Internship/R Code/boundaries_SA1_2011.sqlite",quiet=T)
sa1 <- st_read("C:/Users/Joshua/OneDrive/Documents/Multiviz Internship/1270055001_sa1_2011_aust_shape/SA1_2011_AUST.shp")

sa1_2 <- sa1 %>%
  filter(GCC_NAME11=='Greater Melbourne') %>%
  dplyr::select(sa1=SA1_7DIG11) %>%
  mutate(sa1=as.numeric(sa1))

sa1_centroids <- sa1_2 %>%
  st_centroid()

centroid_orig <- boundaries %>%
  st_drop_geometry() %>%
  inner_join(sa1_centroids, by=c("sa1_id1"="sa1")) %>%
  st_sf() %>%
  st_geometry()

centroid_dest <- boundaries %>%
  st_drop_geometry() %>%
  inner_join(sa1_centroids, by=c("sa1_id2"="sa1")) %>%
  st_sf() %>%
  st_geometry()

distances <- st_distance(centroid_orig,centroid_dest,by_element=TRUE) %>%
  as.numeric()

boundaries_dist <- boundaries %>%
  mutate(distance=distances)

# output here
output_location="C:/Users/Joshua/OneDrive/Documents/Multiviz Internship/R Code/boundaries_SA1_2011_dist.geojson"
st_write(boundaries_dist,output_location,delete_dsn=TRUE)
