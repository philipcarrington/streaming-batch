from datetime import date


def get_meta_data(
        event_type,
        is_client,
        service,
        environment,
        schema_version,
        published,
        organisation='Holiday Extras Limited',
        data_context='batch__streaming'
):
    return {
        "meta": {
            "event": {
                "type": event_type,
                "is_client": is_client,
                "service": service,
                "environment": environment,
                "schema_version": schema_version,
                "published": published,
                "organisation": organisation,
                "data_context": data_context,
            },
            "log": [
                {
                    "system": "publisher",
                    "key": "exit_timestamp",
                    "value": published,
                    "timestamp": published,
                }
            ],
        }
    }


if __name__ == '__main__':
    meta_data = get_meta_data(
        event_type='HXUK_ARRIVAL_DAILY_EXPORT',
        is_client=False,
        service='airflow-data-products',
        environment='production',
        schema_version='1.0.0',
        published=date.today().strftime("%Y-%m-%d %H:%m:%s"),
        organisation='Holiday Extras Limited',
        data_context='batch__streaming'
    )
    print(meta_data)