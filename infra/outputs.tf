output "connection_name" {
  value = google_sql_database_instance.toy_store_instance_terra.connection_name
}

output "database_name" {
  value = google_sql_database.toy_store_terra_db.name
}

output "db_user" {
  value = google_sql_user.toy_terra_user.name
}
