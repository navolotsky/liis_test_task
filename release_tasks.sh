#!/bin/bash
python -m liis_test_task.core.manage migrate
python -m liis_test_task.core.manage loaddata core/fixtures/test_users_and_articles

