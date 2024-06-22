#include <pybind11/pybind11.h>
#include <utility>
#include <deque>
#include <list>

namespace py = pybind11;

class Sensor {
public:
    std::deque<std::pair<long, long double>> records;

    Sensor() {}

    void register_one(long timestamp, long double read) {
        records.push_back(std::make_pair(timestamp, read));
    }

    void register_many(const std::list<std::pair<long, long double>>& list_of_reads) {
        for (const auto& [timestamp, read] : list_of_reads) {
            records.push_back(std::make_pair(timestamp, read));
        }
    }

    py::tuple highest_accumulated() {
        if (records.empty()) {
            return py::make_tuple(-1, -1, -1);
        }

        double max_sum = std::numeric_limits<double>::min();
        double current_sum = 0;
        long max_start = 0;
        long max_end = 0;
        long current_start = 0;

        for (std::size_t i = 0; i < records.size(); ++i) {
            current_sum += records[i].second;

            if (current_sum > max_sum) {
                max_sum = current_sum;
                max_start = current_start;
                max_end = i;
            }

            if (current_sum < 0) {
                current_sum = 0;
                current_start = i + 1;
            }
        }

        return py::make_tuple(records[max_start].first, records[max_end].first, max_sum);
    }
};

PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example plugin"; // Optional module docstring

    py::class_<Sensor>(m, "Sensor")
        .def(py::init<>())
        .def("register_one", &Sensor::register_one)
        .def("register_many", &Sensor::register_many)
        .def("highest_accumulated", &Sensor::highest_accumulated)
        .def_readwrite("records", &Sensor::records);
}
