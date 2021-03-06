from __future__ import print_function
from __future__ import absolute_import

from sandbox.rocky.tf.algos.trpo import TRPO
from rllab.baselines.linear_feature_baseline import LinearFeatureBaseline
from rllab.envs.box2d.cartpole_env import CartpoleEnv
from rllab.envs.normalized_env import normalize
from sandbox.rocky.tf.policies.gaussian_gru_policy import GaussianGRUPolicy
from sandbox.rocky.tf.envs.base import TfEnv
from sandbox.rocky.tf.optimizers.conjugate_gradient_optimizer import ConjugateGradientOptimizer, FiniteDifferenceHvp
from rllab.misc.instrument import stub, run_experiment_lite

stub(globals())

env = TfEnv(normalize(CartpoleEnv()))

policy = GaussianGRUPolicy(
    name="policy",
    env_spec=env.spec,
)

baseline = LinearFeatureBaseline(env_spec=env.spec)

algo = TRPO(
    env=env,
    policy=policy,
    baseline=baseline,
    batch_size=4000,
    max_path_length=100,
    n_itr=10,
    discount=0.99,
    step_size=0.01,
    optimizer=ConjugateGradientOptimizer(hvp_approach=FiniteDifferenceHvp(base_eps=1e-5))
)
run_experiment_lite(
    algo.train(),
    n_parallel=4,
    seed=1,
)
