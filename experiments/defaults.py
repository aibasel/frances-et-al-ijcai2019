import os

from basilisk import BENCHMARK_DIR
from basilisk.steps import PyperplanStep, HeuristicWeightsLPComputation, HeuristicTestingComputation
from sltp.driver import Experiment, generate_pipeline_from_list, \
    ConceptGenerationStep, FeatureMatrixGenerationStep, \
    TransitionSamplingStep
# from sltp.driver import CPPFeatureGenerationStep
from sltp.learn_actions import OptimizationPolicy


heuristic_pipeline = [
    PyperplanStep,
    TransitionSamplingStep,
    ConceptGenerationStep,
    FeatureMatrixGenerationStep,
    # CPPFeatureGenerationStep,
    HeuristicWeightsLPComputation,
    HeuristicTestingComputation,
]


def generate_experiment(domain_dir, domain, **kwargs):
    """ """

    if "instances" not in kwargs:
        raise RuntimeError("Please specify domain and instance when generating an experiment")

    instances = kwargs["instances"] if isinstance(kwargs["instances"], (list, tuple)) else [kwargs["instances"]]
    benchmark_dir = kwargs.get("benchmark_dir", BENCHMARK_DIR)
    kwargs["domain"] = os.path.join(benchmark_dir, domain_dir, domain)
    kwargs["test_domain"] = os.path.join(benchmark_dir, domain_dir, kwargs["test_domain"])
    kwargs["instances"] = [os.path.join(benchmark_dir, domain_dir, i) for i in instances]
    kwargs["test_instances"] = [os.path.join(benchmark_dir, domain_dir, i) for i in kwargs["test_instances"]]

    defaults = dict(
        # Location of the FS planner, used to do the state space sampling
        planner_location=os.getenv("FS_PATH", os.path.expanduser("~/projects/code/fs")),

        # Type of sampling procedure. Only breadth-first search implemented ATM
        driver="bfs",

        # Whether to do IW-like pruning of nodes with novelty higher than the specified (default: -1, no pruning at all)
        # max_width=-1,

        # Whether we are happy to obtain completeness guarantees only with respect to those states
        # that lie in some arbitrary (one) optimal path. Default: False
        complete_only_wrt_optimal=False,

        # Type of sampling. Accepted options are:
        # - "all" (default): Use all expanded states
        # - "random": Use only a random sample of the expanded states, of size given by the option "num_sampled_states"
        # - "optimal": Use those expanded states on some optimal path (only one arbitrary optimal path)
        sampling="all",

        # Number of states to be expanded in the sampling procedure
        num_states=50,

        # Number randomly sampled states among the set of expanded states. The default of None means
        # all expanded states will be used
        num_sampled_states=None,

        # Max. size of the generated concepts (mandatory)
        max_concept_size=10,

        # Max. number of iterations of the concept-generation grammar. Optional. Defaults to infinity,
        # in which case the limit is set by max_concept_size alone.
        max_concept_grammar_iterations=2,

        # Provide a special, handcrafted method to generate concepts, if desired.
        # This will override the standard concept generation procedure (default: None)
        concept_generator=None,

        # Or, alternatively, provide directly the features instead of the concepts (default: None)
        feature_generator=None,

        # A list of features the user wants to be in the abstraction (possibly along others).
        # Default is [], i.e. just run the generation process without enforcing anything
        enforce_features=[],

        # Max. allowed complexity for distance features (default: 0)
        distance_feature_max_complexity=0,

        # Method to generate domain parameters (goal or otherwise). If None, goal predicates will
        # be used (default: None)
        parameter_generator=None,

        # Use the relaxed (weak) increase semantics
        relax_numeric_increase=False,

        # Optionally, use a method that gives handcrafted names to the features
        # (default: None, which will use their string representation)
        feature_namer=default_feature_namer,

        # What optimization criteria to use in the max-sat problem
        optimization=OptimizationPolicy.TOTAL_FEATURE_COMPLEXITY,
        # optimization=OptimizationPolicy.NUM_FEATURES

        # Set a random seed for reproducibility (default: 1)
        random_seed=1,

        # The M parameter of the LP formulation (?)
        lp_max_weight=10,

        domain_dir=domain_dir,

        # The selection strategy to be used when marking which transitions are considered as optimal.
        # - "arbitrary" marks as optimal the transitions in one single path btw initial state
        #  and (some) goal per instance, chosen arbitrarily.
        # "- complete" marks the transitions between all optimal paths btw initial state and (some) goal.
        optimal_selection_strategy="arbitrary",

        # The Experiment class to be used (e.g. standard, or incremental)
        experiment_class=Experiment,

        # The max. number of states in the Flaw set when validating an incremental abstraction
        batch_refinement_size=10,

        # Whether to clean the (sub-) workspaces used to compute incremental abstractions after finishing.
        clean_workspace=True,

        # Reduce output to a minimum
        quiet=False,

        # Validate the computed potential heuristic on the same training set by running hill-climbing until a goal
        validate_learnt_heuristic=True,

        # Whether to take into acount states labeled as unsolvable by whatever planner is being used
        compute_unsolvable_states=True,

        # Whether to prune features that have denotation > 0 over *all states*
        prune_positive_features=False,

        # Whether to prune features that have infinity denotation *in some state*
        prune_infty_features=True,
    )

    parameters = {**defaults, **kwargs}  # Copy defaults, overwrite with user-specified parameters

    steps, parameters = generate_pipeline_from_list(elements=heuristic_pipeline, **parameters)
    exp = parameters["experiment_class"](steps, parameters)
    return exp


def default_feature_namer(s):
    return str(s)
