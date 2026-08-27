import argparse


def main():
    # Imported lazily: `databricks.sdk.runtime` resolves auth at import time,
    # which only succeeds when actually running on a Databricks cluster/job.
    from databricks.sdk.runtime import spark

    # Process command-line arguments
    parser = argparse.ArgumentParser(
        description="Databricks job with catalog and schema parameters",
    )
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    args = parser.parse_args()

    # Set the default catalog and schema
    spark.sql(f"USE CATALOG `{args.catalog}`")
    spark.sql(f"USE SCHEMA `{args.schema}`")


if __name__ == "__main__":
    main()
