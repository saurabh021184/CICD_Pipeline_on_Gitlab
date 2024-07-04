# Database Schema Management for SMAN Project

This guide describes how to perform database schema migrations for the project using Flyway and Docker from a Bastion host.

## Prerequisites

- Docker must be installed on the machine where migrations will be run.
- The user must have network access to the RDS instance from the Bastion host.
- Necessary permissions to execute scripts and access the database.

## Setup

1. Clone the repository and navigate to the `rds-db-migrations` directory:

    ```bash
    # for https clone
    git clone --branch automations https://git.idn.com/lso/automation/response.git

    # for ssh clone
    git clone --branch sman-automations git@git.idn.com:lso/automation/response.git

    cd sman-IAC/rds-db-migrations
    ```

2. Copy the `.env.example` file to `.env`:

    ```bash
    cp .env.example .env
    ```

3. Edit the `.env` file and fill in all the required details such as `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASS`. These details correspond to the database connection information.

## Running Migrations

To run the database migrations, execute the `run_flyway_migration.sh` script:

```bash
./run_flyway_migration.sh


#if you dont have permissions to run the above script run the below command and try again:
chmod +x ./run_flyway_migration.sh
```
```bash
  echo "Starting Flyway migration..."
  docker run --rm \
    -v "${tenant_migrations_path}:/flyway/sql" \
    -w /flyway/sql \
    --env-file "$env_file_path" \
    flyway/flyway migrate
```
