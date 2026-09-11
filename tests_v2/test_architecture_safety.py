from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from predictor_ops.models import EconomicJobKey, JobConfig, JobsFile, JobType, KillSwitchLimits, RiskSnapshot
from predictor_ops.operations import kill_switch_reasons


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_risk_is_rejected(value):
    with pytest.raises(ValidationError):
        RiskSnapshot(daily_loss=value)
    with pytest.raises(ValidationError):
        KillSwitchLimits(max_daily_loss=value)


def test_identity_separator_cannot_create_a_collision():
    with pytest.raises(ValidationError, match="separator"):
        EconomicJobKey(domain="a\x1fb", event_id="c", market="d", decision_stage="e", logical_time=datetime.now(UTC))


def test_generic_v3_job_does_not_need_economic_identity():
    assert JobsFile(schema_version="3", jobs=[JobConfig(id="backup", command=["echo"])]).jobs


def test_defaults_never_authorize_execution():
    job = JobConfig(
        id="execute",
        command=["echo"],
        job_type=JobType.EXECUTION,
        capital_permission=True,
        risk_snapshot=RiskSnapshot(),
    )
    assert set(kill_switch_reasons(job)) >= {
        "risk_snapshot_incomplete",
        "risk_source_unverified",
        "risk_freshness_missing",
        "risk_limits_incomplete",
        "economic_key_missing",
    }


@pytest.mark.parametrize("offset,reason", [(-61, "risk_snapshot_stale"), (1, "risk_snapshot_from_future")])
def test_freshness_is_checked_at_execution_time(offset, reason):
    now = datetime.now(UTC)
    job = JobConfig(
        id="execute",
        command=["echo"],
        job_type=JobType.EXECUTION,
        capital_permission=True,
        risk_source="monitor",
        risk_max_age_seconds=60,
        risk_snapshot=RiskSnapshot(source="monitor", observed_at=now + timedelta(seconds=offset)),
    )
    assert reason in kill_switch_reasons(job, now=now)
